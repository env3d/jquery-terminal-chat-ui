import torch
#from diffusers import FluxPipeline
from PIL import Image

pipe = lambda x, **kwargs: type("MockPipe", (object,),
                                { "images": [ Image.new('RGB', (512,512)) ] })

def init():
  global pipe
  pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev",
                                      torch_dtype=torch.bfloat16,
                                      low_cpu_mem_usage=True)
  pipe.to('cuda')  

prompt = "A cat holding a sign that says hello world"
def gen(prompt, filename="static/output.png", steps=50, guidance=3.5):
  image = pipe(
      prompt,
      height=512,
      width=512,
      guidance_scale=guidance,
      num_inference_steps=steps,
      max_sequence_length=512,
      generator=torch.Generator('cpu').manual_seed(torch.randint(0, 2**32, (1,)).item())
  ).images[0]
  image.save(filename)