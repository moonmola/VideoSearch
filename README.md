# yolo와 객체 추적을 이용한 동영상 검색 기능
객체 인식에 기반한 동영상 검색 기능을 제공

> 데이터분석 캡스톤디자인 프로젝트로 진행되었습니다.

<br>

## 1. 프로젝트의 목표 및 내용
유튜브의 성장으로 동영상 중심의 콘텐츠 소비가 늘어가고 있다. 이에 따라 텍스트가 아닌 동영상을 통해 정보를 확인하는 검색 형태가 증가하고 있다. 사용자가 원하는 장면을 객체인식통해 찾아주는 기능을 개발한다면 유용하게 쓰일것으로 예상된다.   

<br><br>
## 2. Experiment
- Qt Designer로 레이아웃을 편집하였으며 PyQt라이브러리로 구현하였습니다.

### 1) YOLO
<img src=https://user-images.githubusercontent.com/55346446/102999680-d3f89400-456c-11eb-94d7-1afc93a17fd3.png width="150">
검색하고자 하는 객체의 이름을 넣고 검색버튼을 누른다.
cfg파일은 네트워크의 layout을 block단위로 정의해놓은 파일이다.
 
괄호들은 하나의 네트워크적인 의미를 가지고 있고 Yolo에서는 convolutional, shortcut, upsample, route, Yolo,Net 총 6타입의 layer들이 있다. 
  Yolo 레이어를 살펴보면 mask 값을 리스트에 저장하고 anchors 값을 파싱하고 mask에 있는 값만 남긴다.
그 값을 DetectionLayer에서 사용한다. 바운딩 박스들을 저장하기 위해 Detection Layer를 생성한다.


### 2) Object Tracking
Tracking은 주변 환경에서 일어나는 이미지의 움직임, 경로(Path)를 추적하는 문제로 정의 할 수 있다. 영상의 single frame의 환경에서 객체의 움직임을 찾을 때, route를 생성해가는 과정을 거친다.
<img src=https://user-images.githubusercontent.com/55346446/102999738-f38fbc80-456c-11eb-98b0-b9fba710d74a.png width="600">
1) Initialization : 이 과정은 컨테이너에 아무것도 없을 시 각 Class마다 딱 한번 시행 된다.<br>
trackers라는 container에 담긴 정보가 하나도 없을 경우 'datFrameData.box'라는 곳의 박스 정보를 넣게 된다. 칼만필터를 작동 시켜야 하는데 칼만 필터는 이전 데이터를 가지고 predict(예측) 과정 연산을 하게 되는데 아무것도 없을 경우 그냥 현재 Detection된 Box의 정 보로 초기화를 해야하기 때문이다.<br>
2) Prediction : 칼만필터에서 Predict 하는 과정이다. 결과 값으로는 Xp(예측값), Pp(예측 오차공 분산)이 나온다.
3) IoU : 이전 Box 정보가 현 frame에서 같은 ID라고 매칭 시키는 방법이다. Prediction값(이전 데이터를 통해 예측된 값)과 방금 들어온 Detection Box들이 'GetIOU'라는 함수로 들어가서 iouMatrix에 저장이 된다. IoU란 Intersection over Union의 약자로 '교집합(두개의 박스가 겹 치는 부분의 면적) / 합집합(두개의 박스의 모든 면적)'의 결과물이 비율로 나오게 되어 이 점 수가 크면 확률상 같은 ID라고 판단 할 수 있다. score가 클수록 더 사각형이 일치한다.<br>
4) Hungarian : 비용(연산량)을 최소화 시키는 할당 시키는 최적 matching 알고리즘이다. 매칭이 이루어 진 정보는 'assignment'에 담긴다.

<br><br>
## 3. 기능 및 UI
- Qt Designer로 레이아웃을 편집하였으며 PyQt라이브러리로 구현하였습니다.

### 1) 메인화면
<img src=https://user-images.githubusercontent.com/55346446/102999159-e0302180-456b-11eb-8a6f-6b37cb925dd0.png width="600">
검색하고자 하는 객체의 이름을 넣고 검색버튼을 누른다.

### 2) 검색화면
<img src=https://user-images.githubusercontent.com/55346446/102999267-0fdf2980-456c-11eb-93f7-2aa82fff7f0f.png width="600">
동영상에서 객체를 검색하여 객체 목록에 전체 동영상에서 객체가 검출되는 부분만 보여준다. 재생버튼을 클릭하면 영상으로 확인할 수 있다.

<br><br>

