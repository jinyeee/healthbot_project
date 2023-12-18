function goToHospital(){
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8080/hospital',
        dataType: 'json', 
        contentType: 'application/json',
        data : {"department" : "내과"}, //데이터 임시로 지정
        success: function (result) {
            localStorage.setItem('hospitalList', JSON.stringify(result))
            location.href='hospital.html'
        },
        error: function (result, status, error) {
            console.log(error)
        }
    });
}

const storedData = localStorage.getItem('hospitalList'); // 스토리지에 저장해둔 데이터, 
const hospitalResult = JSON.parse(storedData); //가져온 데이터를 javaScript객체로 변환
document.querySelector('#tbody').innerHTML = '';

let str = '';

for(let review of hospitalResult){
    //alert(review.hospitalId);


     // str += '그릴 그림 코드로 작성';

    str += '<tr>';
    str += `    <td>${review.hospitalId}</td>`;
    str += `    <td><a onclick="test('${review.hospitalId}')" data-bs-toggle="modal" data-bs-target="#exampleModal">${review.hospitalName}</a></td>`;
    str += '    <td>56%</td>';
    str += '    <td>44%</td>';
    str += '    <td>78개</td>';

    // str += '<a data-bs-toggle="modal" data-bs-target="#exampleModal">';
    // str += 'Launch demo modal';
    // str += '</a>';

    str += '</tr>';
}


// <!-- Button trigger modal -->
// <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
//   Launch demo modal
// </button>

document.querySelector('#tbody').innerHTML = str;

// $.each(hospitalResult, function(i) {
//     console.log(i);
// })


// $.each(hospitalResult, function(i) {
//     console.log(i);
// })


// $.each(JSON.parse(myData), ...);

function test(hospitalId){

    alert(hospitalId);
}