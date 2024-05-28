import logging
import pprint
import numpy as np
from PIL import Image
from giza.agents import GizaAgent


# Process the image
def process_image(img):
    img = np.resize(img, (28,28))
    img = img.reshape(1,1,28,28)
    img = img/255.0
    print(img.shape)
    # For now, we will just use a small tensor as input to a single-layer softmax. We will change this when the PoC works
    tensor = np.random.rand(1,3)
    return tensor
    
# Get the image
def get_image(path):
    with Image.open(path) as img:
        img = img.convert('L')
        img = np.array(img)
    return img

# Create the execution function
def transmission():
    logger = logging.getLogger(__name__)
    img_path = 'seven.png'
    img = get_image(img_path)
    img = process_image(img)
    id = ...
    version = ...
    account = ...
    contract_address = "0x17807a00bE76716B91d5ba1232dd1647c4414912"

    agent = GizaAgent(
        contracts={"mnist": contract_address},
        id=id,
        chain="ethereum:sepolia:geth",
        version_id=version,
        account=account
    )

    result = agent.predict(input_feed={"image": img}, verifiable=True)

    logger.info(f"Result: {result}")
    with agent.execute() as contracts:
        logger.info("Executing contract")
        contract_result = contracts.mnist.mint(int(result.value[0].argmax()))
        logger.info("Contract executed")

    logger.info(f"Contract result: {contract_result}")
    pprint.pprint(contract_result.__dict__)
    logger.info("Finished")

transmission()