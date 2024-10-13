# main.py

from fastapi import FastAPI
import makenoise as mn

app = FastAPI()

@app.get("/bark/{sound_file}")
async def bark(sound_file: str ):
    sound_files = ['mixkit-dog-barking-twice-1.wav','mixkit-giant-dog-aggressive-growl-59.wav', 'mixkit-hellhound-monster-attack-dog-wolf-creature-3015.wav']  
    await mn.dog_bark(sound_file)
    return (f'Barking 1: {sound_file}')