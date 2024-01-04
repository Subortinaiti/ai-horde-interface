## ImaGen Class
The ImaGen class is a Python implementation designed to interact with the stable horde API for generating images. It provides functionalities to submit image generation requests, check the status of the requests, and retrieve the generated images. Below is an overview of the key features and usage of the ImaGen class.

## Features:
Image Generation:

Submits image generation requests to the stable horde API.
Allows customization of various parameters such as prompt, image dimensions, number of steps, and more.
Request Status Checking:

Retrieves the status of a previously submitted image generation request.
Provides information such as processing status, queue position, kudos, and whether the generation is complete.
Image Retrieval:

Extracts and saves generated images once the generation process is complete.
Supports saving multiple images with customizable filenames and paths.
Usage Example:


    if __name__ == "__main__":
        gen = ImaGen()
    
        print("Sending generation request...")
        reqid = gen.generate(prompt="a white square on a black background", n=1)
    
        print(f"Generation request sent! (id: {reqid})")
        done = False
        while not done:
            status = gen.status()
            print(status)
            if status["done"]:
                done = True
        gen.extract_done("generated_image", "output_path")
        print("Done!")

    
## Dependencies:
The class utilizes the requests library for making HTTP requests.
ListModels Function
The ListModels function is a utility function designed to retrieve a list of available image models from thestable horden API. It provides a simple way to fetch and display the available models.

## Model Listing Feature:

Sends a GET request to the stable horde API to fetch information about available image models.
Extracts and returns a list of model names.

Usage Example:


    models = ListModels()
    print("Available Image Models:")
    for model in models:
        print(model)

