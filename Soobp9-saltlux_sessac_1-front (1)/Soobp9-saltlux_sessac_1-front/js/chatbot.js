function sendMessage() {
  var messageInput = document.getElementById('message-input');
  var chatBox = document.getElementById('chat-box');

  if (messageInput.value.trim() !== '') {
    // 나의 메시지
    chatBox.innerHTML += '<div class="message my-message"><strong>나:</strong> ' + messageInput.value + '</div>';
    messageInput.value = '';

    // 상대의 응답 (임의로 "상대"로 고정된 메시지)
    setTimeout(function() {
      chatBox.innerHTML += '<div class="message other-message"><strong>상대:</strong> 안녕하세요!</div>';
      chatBox.scrollTop = chatBox.scrollHeight; // 스크롤을 항상 아래로 조정
    }, 500); // 0.5초 후에 응답이 오도록 설정 (시뮬레이션용)
  }
}

const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})

$('#testBtn').click(function(e){
    e.preventDefault();
    $('#testModal').modal("show");
});






// const chatbotBtn = document.getElementById('chatbotBtn');
//  var department = document.getElementById('department').value;

// chatbotBtn.addEventListener('click', (event) => {
//     event.preventDefault();
//     // alert(department);

//         $.ajax({
//             type: 'GET',
//             url: 'http://localhost:8080/hospital',
//             // dataType: 'json', // 서버에서 준 데이터 형식
//            // contentType: 'application/json',
//           //  data: JSON.stringify(loginDto),
//             data : {"department" : "내과"}, 
//             success: function (result) {
//                 console.log(result)
//                 alert(result)
               
                
//             },
//             error: function (result, status, error) {
//                 console.log(error)
//             }
//         });
//  });

