import json
from web3 import Web3
from giza_actions.model import GizaModel
from typing import Optional
import requests
from ape import Contract
from ape_accounts import import_account_from_mnemonic, accounts
from ape.types.signatures import recover_signer
from asyncer import asyncify
import logging
from giza.frameworks.cairo import verify

class GizaAgent:
    """
    A blockchain AI agent that helps users put their Actions on-chain. Uses Ape framework and GizaModel to verify a model proof off-chain, sign it with the user's account, and send results to a select EVM chain to execute code.

    Attributes: FINISH THESE
        model (GizaModel): The model that this deployer uploads proofs for. This model must have the following fields: model_path, id, version, orion_runner_service_url in order to work. This is because all on-chain models require a proof to be generated by Orion Runner.
        inference: The result of the GizaModel inference
        request_id: The request_id of the proof to fetch from the GCP
        proof: The proof from GCP that we will use to verify, sign, and send along with inference data
        

    Methods:
        infer: Runs model inference and retrieves the model output
        get_model_data: retrieves the proof from GCP given the request_id, version_id, deployment_id, and internal model_id
        process_inference: overriden by user to specify calldata for a given smart contract function
        verify: verifies the proof locally
        deploy: verifies the proof, then calls the smart contract with calldata from inference
    """
    
    def __init__(self, model: GizaModel):
        """Initialize deployer.
        
        Args:
            model (GizaModel): GizaModel instance
        """
        if (
            model.model_path is None
            or model.id is None
            or model.version is None
        ):
            raise ValueError(
                "GizaModel is missing required fields: "
                "model_path, id, version"
            )

        self.model = model

    def infer(self, input_file: Optional[str], input_feed: Optional[dict]):
        """Run model inference and store output."""
        (self.inference, self.request_id) = self.model.predict(input_file, input_feed, verifiable=True)
        print("Inference saved! ✅ Result: ", self.inference, self.request_id)
        
    @asyncify
    def _get_model_data(self):
        """Get proof data from GCP and save it as a class attribute"""
        
        uri = self.model.get_deployment_uri()
        proof_metadata_url = f"https://api-dev.gizatech.xyz/api/v1/models/{self.model.id}/versions/{self.model.version}/deployments/{uri}/proofs/{self.request_id}"

        response = requests.get(proof_metadata_url)
        
        logging.info(f"Response status code: {response.status_code}")
        logging.debug(f"Full response: {response.text}")

        if response.status_code == 200:
            proof_metadata = response.json()
            self.proof = proof_metadata
            return proof_metadata
        else:
            raise Exception(f"Failed to get proof metadata: {response.text}")

    def generate_calldata(self, abi_path, function_name, parameters):
        """
        Generate calldata for calling a smart contract function

        Args:
            abi_path (str): Path to JSON ABI for the contract
            function_name (str): Name of contract function to call 
            parameters (list): Arguments to pass to the function

        Returns:
            str: Hex string of calldata
        """
        with open(abi_path, 'r') as f:
            abi = json.load(f)
        
        web3 = Web3()
        contract = web3.eth.contract(abi=abi)
        
        function_abi = next((x for x in abi if x['name'] == function_name), None)
        if function_abi is None:
            raise ValueError(f"Function {function_name} not found in ABI")
            
        calldata = contract.encodeABI(function_name, args=parameters)
        return calldata
    
    @asyncify
    def verify(self, proof):
        """
        Verify proof locally. Must be run *after* infer() and _get_model_data() have been run.
        
        Returns:
            bool: True if proof is valid
        """
        model_id = self.model.id
        version_id = self.model.version
        try:
            # Beware of JobSize = JobSize.S
            result = verify(proof, model_id, version_id)
            if result is None:
                return True
            else:
                return False
        except BaseException:
            logging.error("An error occurred when verifying")
            return False
        
    # todo: We may want to avoid passing passphrase and mnemonic for security purposes
    @asyncify
    def transmit(self, account, sc_address: str, sc_abi_path: str, model: GizaModel, proof, signed_proof, calldata: str):
        """
        Transmit: Verify the model proof, 
        
        Returns:
            A transaction receipt
        """    
        # Verify the user's proof
        assert model.verify(proof)
        # Verify the signature
        recovered_signer = recover_signer(proof, signed_proof)
        assert recovered_signer == account.address
        # Create contract instance
        contract = Contract(sc_address, abi=sc_abi_path)
        # Call the contract
        try:
            receipt = contract.call(calldata, account)
            if not receipt.failed:
                return receipt
        except Exception as e:
            raise Exception(f"Transaction failed: {e}")