from transformers import SeamlessM4Tv2ForTextToSpeech , AutoProcessor 
import torch , numpy as np


class TransformersProcessor:
    def __init__(self) -> None:
        self.model = SeamlessM4Tv2ForTextToSpeech.from_pretrained("facebook/seamless-m4t-v2-large",torch_dtype=torch.float16)
        self.processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
        self.model.to(self.device)
        

    def process(self,message:str) -> bytes:
        device = torch.device('cuda')
        self.model.to(device)
        text_inputs = self.processor(text = message, src_lang="arb", return_tensors="pt").to(device)
        audio_array_from_text = self.model.generate(**text_inputs, tgt_lang="arb",speaker_id=10)[0].cpu().numpy().squeeze()
        return audio_array_from_text

    def ProcessAndWriteFile(self,message:str, file_path:str="out_from_text.wav") -> None:
        import scipy
        device = torch.device('cuda')
        self.model.to(device)
        text_inputs = self.processor(text = message, src_lang="arb", return_tensors="pt").to(device)
        audio_array_from_text = self.model.generate(**text_inputs, tgt_lang="arb",speaker_id=10)[0].cpu().numpy().squeeze()
        sample_rate = self.model.config.sampling_rate
        scipy.io.wavfile.write(file_path, rate=sample_rate, data=audio_array_from_text.astype(np.float32))



