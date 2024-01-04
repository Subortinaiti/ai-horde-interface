import requests
import json


def ListModels():
    response = requests.get("https://stablehorde.net/api/v2/status/models?type=image")
    models = [r["name"] for r in response.json()]
    return models

def save_image(image_link,final_filename,save_path=""):
    response = requests.get(image_link)
    with open(f"{save_path}{final_filename}.webp", "wb") as f:
        f.write(response.content)




class RequestData:
    def __init__(self):
        self.api_key = "0000000000"
        self.imgen_params = {
            "n": 2,
            "width": 64*8,
            "height": 64*8,
            "steps": 20
        }
        self.submit_dict = {
            "prompt": "a white question mark with a black background",
            "nsfw": False,
            "censor_nsfw": False,
            "trusted_workers": False,
            "models": ["stable_diffusion"],
            "r2": True,
            "dry_run": False
        }

    def get_submit_dict(self):
        submit_dict = self.submit_dict.copy()
        submit_dict["params"] = self.imgen_params
        return submit_dict




class ImaGen:
    def __init__(self):
        pass # this is useless, but might get used in the future

    def generate(self,api_key=None, prompt=None, nsfw=None, censor_nsfw=None,
                 trusted_workers=None, models=None, r2=None, dry_run=None,
                 n=None, width_mult=None, height_mult=None, steps=None,save_path=""):

        request_data = RequestData()
        self.done = False
        
        # Update RequestData with provided values
        if api_key:
            request_data.api_key = api_key
        if n:
            request_data.imgen_params["n"] = n
        if width_mult:
            request_data.imgen_params["width"] = width_mult*64
        if height_mult:
            request_data.imgen_params["height"] = height_mult*64
        if steps:
            request_data.imgen_params["steps"] = steps
        if prompt:
            request_data.submit_dict["prompt"] = prompt
        if nsfw is not None:
            request_data.submit_dict["nsfw"] = nsfw
        if censor_nsfw is not None:
            request_data.submit_dict["censor_nsfw"] = censor_nsfw
        if trusted_workers is not None:
            request_data.submit_dict["trusted_workers"] = trusted_workers
        if models:
            request_data.submit_dict["models"] = models
        if r2 is not None:
            request_data.submit_dict["r2"] = r2
        if dry_run is not None:
            request_data.submit_dict["dry_run"] = dry_run

        headers = {
            "apikey": request_data.api_key,
            "Client-Agent": "cli_request_dream.py:1.1.0:(discord)db0#1625",    # the original file had this so I put it in as well, i think it's needed
        }


        submit_req = requests.post('https://aihorde.net/api/v2/generate/async',
                                   json=request_data.get_submit_dict(), headers=headers)

        if submit_req.ok:
            submit_results = submit_req.json()
            req_id = submit_results.get('id')

            self.req_id = req_id
            self.submit_results = submit_results
            
            if not req_id:
                print(submit_results)
                return False
            return req_id


    def status(self):
        chk_req = requests.get(f'https://aihorde.net/api/v2/generate/check/{self.req_id}')
        if not chk_req.ok:
            print(chk_req.text)
            return False
        chk_results = chk_req.json()
        if chk_results["done"]:
            self.done = True

        # THIS LOOKS SOMETHING LIKE THIS:
        # {finished': 0, 'processing': 0, 'restarted': 0, 'waiting': 1, 'done': False,
        # 'faulted': False, 'wait_time': 24, 'queue_position': 39, 'kudos': 1.0, 'is_possible': True}     
        return chk_results       


    def extract_done(self,imagename = "generated_image",imagepath=""):
        self.status()   # update the "done" flag, it's stupid but it's simple
        if self.done:    
            retrieve_req = requests.get(f'https://aihorde.net/api/v2/generate/status/{self.req_id}')
            if not retrieve_req.ok:
                print(retrieve_req.text)
                return None

            results_json = retrieve_req.json()
            results = results_json['generations']        

            for iter in range(len(results)):
                final_filename = f"{imagepath}{imagename}_{iter+1}"
                b64img = results[iter]["img"]
                image_link = b64img.encode('utf-8')

                save_image(image_link, final_filename)

            return results





if __name__ == "__main__":
    gen = ImaGen()

    print("sending generation request...")
    reqid = gen.generate(prompt="None",n=1)

    print(f"generation request sent! (id:{reqid})")
    done = False
    while not done:
        R = gen.status()
        print(R)
        if R["done"]:
            done = True
    gen.extract_done("eggus")
    print("done!")




