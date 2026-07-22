import io

import numpy as np
import streamlit as st

try:
    from resemblyzer import VoiceEncoder, preprocess_wav
except ModuleNotFoundError:
    VoiceEncoder = None
    preprocess_wav = None

try:
    import librosa
except ModuleNotFoundError:
    librosa = None


def voice_features_available():
    return VoiceEncoder is not None and preprocess_wav is not None and librosa is not None


@st.cache_resource
def load_voice_encoder():
    if not voice_features_available():
        return None
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    if not voice_features_available():
        st.info('Voice features are unavailable in this environment, so no voice embedding was created.')
        return None

    try:
        encoder = load_voice_encoder()
        if encoder is None:
            return None

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception:
        st.warning('Voice recognition is unavailable right now. The profile was saved without a voice embedding.')
        return None
    
def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0
    
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score

def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    if not voice_features_available():
        return {}

    try:
        encoder = load_voice_encoder()
        if encoder is None:
            return {}

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                identified_results[sid] = max(identified_results.get(sid, 0.0), score)

        return identified_results
    except Exception:
        st.warning('Bulk audio processing is unavailable right now.')
        return {}