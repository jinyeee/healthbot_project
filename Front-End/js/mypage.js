

window.onload = function(){
    const userSequence = JSON.parse(localStorage.getItem("userInfo")).userSeq;
    console.log(userSequence);
    $.ajax({
        type: 'GET',
        url: `http://localhost:8080/mypage/${userSequence}`,
        dataType: 'json', // 서버에서 준 데이터 형식
        // data: JSON.stringify(userSequence),
        contentType: 'application/json',
        //data: {"":1},
        success: function (result) {
            console.log(result);
            document.querySelector('#userInfoCard').innerHTML = '';

            let str = '';
                      str += ``;
                      str += `<p><strong>아이디:</strong>${result.userId}</p>`;
                      str += `<p><strong>성별:</strong>${result.userGender}</p>`;
                      str += `<p><strong>나이:</strong>${result.userAge}</p>`;
      
            document.querySelector('#userInfoCard').innerHTML = str; 
        },
        error: function (result, status, error) {
            console.log(error)
        }
        
    });
}


 
 // 페이지 로드 시 개인 정보 섹션을 표시
 document.addEventListener("DOMContentLoaded", function() {
    showInfo();
});

function showInfo() {
    document.getElementById('infoSection').style.display = 'block';
    document.getElementById('recordsSection').style.display = 'none';
    const storedUserInfo = localStorage.getItem('userInfo');
    const userInfo = JSON.parse(storedUserInfo); 
    document.querySelector('#userInfoCard').innerHTML = '';

      let str = '';
                str += ``;
                str += `<p><strong>아이디:</strong>${userInfo.userId}</p>`;
                str += `<p><strong>성별:</strong>${userInfo.userGender}</p>`;
                str += `<p><strong>나이:</strong>${userInfo.userAge}</p>`;

    document.querySelector('#userInfoCard').innerHTML = str;            
    // alert(userInfo.userName);
}

function showRecords() {
    document.getElementById('infoSection').style.display = 'none';
    document.getElementById('recordsSection').style.display = 'block';
}
