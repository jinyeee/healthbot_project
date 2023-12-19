const storedData = localStorage.getItem('userInfo');
const userInfoResult = JSON.parse(storedData);

console.log(userInfoResult);
document.querySelector('#user').innerHTML = `${userInfoResult.userId}님 환영합니다.`;


const userAge = userInfoResult.userAge;
const userGender = userInfoResult.userGender;


var dongInfo = $("#dong option:selected").val();
var department = '';
//****동 주소 데이터 세팅 */
//selectBox 변경 시 실행
var selectBoxChange = function (dongData) {
  console.log("dong : " + dongData);
  dongInfo = dongData;
}

document.addEventListener('DOMContentLoaded', function () {
  var messageInput = document.getElementById('message-input');
  messageInput.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });
});

function sendMessage() {
  var messageInput = document.getElementById('message-input');
  var chatBox = document.querySelector(".middle")
  if (messageInput.value.trim() !== '') {
    // 나의 메시지
    chatBox.innerHTML += `<div class="outgoing">
                            <div class="texts">
                              <div class="bubble">${messageInput.value}</div>
                            </div>
                          </div>`
    const userMessage = messageInput.value;
    messageInput.value = '';

    $.ajax({
      url: 'http://127.0.0.1:8000/chatbot/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ "utterance": userMessage }),
      success: function (data) {
        //데이터 department 존재 유무로 메세지 append 다르게 진행
        console.log(data)
        chatBox.innerHTML += `<div class="incoming">
                                <div class="bot_incoming">
                                  <img src="/images/doctor.png" alt="" width="50" height="50">
                                  <div class="texts">
                                    <strong class="bubble">${data.bot_message}</strong>
                                  </div>
                                </div>
                                `;
        if (data.department != '') {
          console.log("진료과 존재")
          chatBox.innerHTML += `<div>
                                  <button class="hospitalBtn hospitalBtn-3" onclick="goHospitalList()">추천 병원 보기</button>
                                </div>
                              `;
          department = data.department;
        }
        chatBox.innerHTML += `</div>` 
        chatBox.scrollTop = chatBox.scrollHeight;
      },
      error: function (error) {
        console.error('Error:', error);
      }
    });
  }
}

function goHospitalList(){
  window.location.href = `hospital.html?department=${department}&location=${dongInfo}`;
}


function getAllHospital(){
  window.location.href = `hospital.html?location=${dongInfo}`;
}





