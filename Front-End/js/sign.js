const loginBtn = document.getElementById('form_btn');
const joinBtn = document.getElementById('join_btn');

loginBtn.addEventListener('click', (event) => {
    event.preventDefault();
    const loginDto = {
        "userId" : $('#signId').val(),
        "userPw" : $('#signPw').val()
    };
    $.ajax({
        type: 'POST',
        url: 'http://localhost:8080/sign/login',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(loginDto),
        success: function (result) {
            console.log(result)
            if(result.result == 'success'){
              
                console.log(result)
                const userInfo = {
                    "userId": $('#signId').val(),
                    "userSeq": result.userSeq
                }
                localStorage.setItem("userInfo", JSON.stringify(userInfo))
                location.href = '/html/chatbot.html'
            }
            else{
                alert('잘못 입력되었습니다. \n회원 정보를 다시 확인해 주세요')
                location.href = '/html/sign.html'
            } 
        },
        error: function (result, status, error) {
            console.log(error)
        }
    });
});


joinBtn.addEventListener('click', (event) => {
    console.log("회원가입")
    event.preventDefault();

    var gender = document.getElementsByName('gender');
    var genderChoice; 
    for(var i=0; i<gender.length; i++) {
         if(gender[i].checked) {
        userGender = gender[i].value;
        }
    }

    const userDto = {
        "userId" : $('#userId').val(),
        "userPw" : $('#userPw').val(),
        "userAge" : $('#userAge').val(),
        "userGender" : userGender
    };

    console.log(userDto)

    $.ajax({
        type: 'POST',
        url: 'http://localhost:8080/sign',
        contentType: 'application/json',
        data: JSON.stringify(userDto),
        success: function (result) {
            if(result == 'success'){
                console.log(result)
                alert('회원가입이 완료되었습니다.')
                location.href = '/html/sign.html'
            }
            else{
                alert('가입에 실패했습니다. \n정보를 다시 확인해 주세요')
                location.href = '/html/sign.html'
            } 
        },
        error: function (result, status, error) {
            console.log(error)
        }
    });
    



});


const signUpBtn = document.getElementById("signUp");
const signInBtn = document.getElementById("signIn");
const container = document.querySelector(".container");

signUpBtn.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});
signInBtn.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

