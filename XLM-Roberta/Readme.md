

# XLM-Roberta 
### xlm-roberta-large <br/><br/>

- - -
## 학습 데이터 
#### [한국어 단발성 대화](https://aihub.or.kr/opendata/keti-data/recognition-laguage/KETI-02-009)<br/><br/>

- - -
### 파라미터  
#### batch_size = 32
#### MAX_LEN = 32
#### num_epochs = 5
#### Learning rage(Adam) = 1e-5
<br/><br/>

### 학습 결과
### 학습 데이터 정확도 : 0.5989 / 테스트 데이터 정확도 0.5707<br/><br/>
- - -

### 파라미터  
#### batch_size = 128
#### MAX_LEN = 12
#### num_epochs = 5
#### Learning rage(Adam) = 1e-8
<br/><br/>

### 학습 결과
### 학습 데이터 정확도 : 0.4776 / 테스트 데이터 정확도 0.4983<br/><br/>
- - -
### 파라미터  
#### batch_size = 32
#### MAX_LEN = 32
#### num_epochs = 7
#### Learning rage(Adam) = 1e-5
<br/><br/>

### 학습 결과
### 학습 데이터 정확도 : 0.6447 / 테스트 데이터 정확도 0.5597<br/><br/>
- - -
### 파라미터  
#### batch_size = 32
#### MAX_LEN = 32
#### num_epochs = 7
#### Learning rage(Adam) = 1e-5
#### attention_probs_dropout_prob = 0.2
#### hidden_dropout_prob = 0.2
<br/><br/>

### 학습 결과
### 학습 데이터 정확도 : 0.4277 / 테스트 데이터 정확도 0.5673<br/><br/>
- - -


## [참고](https://dacon.io/en/competitions/official/235875/codeshare/4539?page=1&dtype=recent)
