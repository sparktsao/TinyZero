# TinyZero - ScamR1: Reasoning but Don't Think Too Much  
![image](cover.png)  

TinyZero - ScamR1 extends [TinyZero](https://github.com/Jiayi-Pan/TinyZero) into **SCAM reasoning and detection**, enhancing cybersecurity applications.  

## 🔍 Key Enhancements  

### 1️⃣ SCAM Reasoning & Detection  
- **Scam Data Generator**: Creates synthetic scam scenarios for training  
- **Reward Scoring**: Improves scam detection accuracy through RL  

### 2️⃣ Results & Observations  
- **Validation confirms no overfitting**  
- **Significant improvements in the first 200 steps**, particularly in **format alignment**  
- **Response length stabilizes at ~150 tokens**, after an initial reduction  

## ⚙️ Installation  

```bash  
conda create -n zero python=3.9  
pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu121  
pip install vllm==0.6.3 ray  
pip install -e .  # verl  
pip install flash-attn --no-build-isolation  
pip install wandb IPython matplotlib  
```

## 🚀 SCAM Task  

### 🛠 Data Preparation  

```bash  
conda activate zero  
python ./examples/data_preprocess/scam.py --local_dir {path_to_your_dataset}  
```

### 🎯 Run Training  

```bash  
conda activate zero  
export N_GPUS=2  
export BASE_MODEL={path_to_your_model}  
export DATA_DIR={path_to_your_dataset}  
export ROLLOUT_TP_SIZE=2  
export EXPERIMENT_NAME=scam-detection  
export VLLM_ATTENTION_BACKEND=XFORMERS  

bash ./scripts/train_tiny_zero.sh  
```

## 🔗 Acknowledgments  

- Built upon [TinyZero](https://github.com/Jiayi-Pan/TinyZero)  
- Uses the [veRL](https://github.com/volcengine/verl) framework  

## 📜 Citation  

If referencing this work, please cite:  

```bibtex  
@misc{tinyzero_scamr1,  
  author       = {Spark Tsao},  
  title        = {TinyZero - ScamR1: Reasoning but Don't Think Too Much},  
  howpublished = {https://github.com/SparkTsao/TinyZero-ScamR1},  
  note         = {Accessed: 2025-02-22},  
  year         = {2025}  
}  
```

