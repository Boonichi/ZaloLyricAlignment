import torch
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import soundfile as sf
import librosa
import scipy
import json
import os
import random
import requests
from time import sleep
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from dataclasses import dataclass
from demucs import pretrained
from demucs.apply import apply_model
from demucs.audio import convert_audio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from unidecode import unidecode