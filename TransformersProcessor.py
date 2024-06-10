from transformers import SeamlessM4Tv2ForTextToSpeech , AutoProcessor 
import torch , numpy as np


class TransformersProcessor:
    def __init__(self) -> None:
        self.model = SeamlessM4Tv2ForTextToSpeech.from_pretrained("facebook/seamless-m4t-v2-large",torch_dtype=torch.float16)
        self.device = torch.device('cuda')
        self.model.to(self.device)
        self.processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")

    def process(self,message:str) -> bytes:
        text_inputs = self.processor(text = message, src_lang="arb", return_tensors="pt").to(self.device)
        audio_array_from_text = self.model.generate(**text_inputs, tgt_lang="arb",speaker_id=10)[0].cpu().numpy().squeeze()
        return audio_array_from_text

    def ProcessAndWriteFile(self,message:str, file_path:str="out_from_text.wav"):
        import scipy
        text_inputs = self.processor(text = message, src_lang="arb", return_tensors="pt").to(self.device)
        audio_array_from_text = self.model.generate(**text_inputs, tgt_lang="arb",speaker_id=10)[0].cpu().numpy().squeeze()
        sample_rate = self.model.config.sampling_rate
        scipy.io.wavfile.write(file_path, rate=sample_rate, data=audio_array_from_text.astype(np.float32))



