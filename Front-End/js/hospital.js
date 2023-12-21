const urlParam = new URL(location).searchParams;
const department = urlParam.get("department");
const dong = urlParam.get("location");
console.log(department + " " + dong);

window.onload = function () {
    console.log("?????");
    if (department == null) {
        $(".title").append(`<h1>${dong} 추천 병원</h1>`)
        $.ajax({
            type: 'GET',
            url: `http://localhost:8080/hospital/find?location=${dong}`,
            dataType: 'json',
            contentType: 'application/json',
            success: function (result) {
                console.log("모든 병원")
                console.log(result)
                let str = '';

                for (let hospital of result) {
                    str += '<tr>';
                    str += `    <td><a onclick="hospitalInfo('${hospital.hospitalId}')">${hospital.hospitalName}</a></td>`;
                    str += `    <td>${hospital.positivePercentage}%</td>`;
                    str += `    <td>${hospital.negativePercentage}%</td>`;
                    str += `    <td>${hospital.reviewTotalCnt}</td>`;
                    str += '</tr>';
                }
    
                document.querySelector('#tbody').innerHTML = str;
            },
            error: function (result, status, error) {
                console.log(error)
            }
        });
    }else{
        $(".title").append(`<h1>${dong} ${department} 추천 병원</h1>`)
        $.ajax({
            type: 'GET',
            url: `http://localhost:8080/hospital/find?department=${department}&location=${dong}`,
            dataType: 'json',
            contentType: 'application/json',
            success: function (result) {
                let str = '';

                for (let hospital of result) {
                    str += '<tr>';
                    str += `    <td><a onclick="hospitalInfo('${hospital.hospitalId}')">${hospital.hospitalName}</a></td>`;
                    str += `    <td>${hospital.positivePercentage}%</td>`;
                    str += `    <td>${hospital.negativePercentage}%</td>`;
                    str += `    <td>${hospital.reviewTotalCnt}</td>`;
                    str += '</tr>';
                }
    
                document.querySelector('#tbody').innerHTML = str;
            },
            error: function (result, status, error) {
                console.log(error)
            }
        });
    }
    
    
}

function hospitalInfo(hospitalId) {
    $.ajax({
        type: 'GET',
        url: `http://localhost:8080/hospital/${hospitalId}`,
        dataType: 'json',
        contentType: 'application/json',
        success: function (hospitalInfo) {
          
            let str = '';
            str += '<div id="map" style="width:100%; height: 350px;"></div>';
            str += '<div>';
            str += '    <table class="table">';
            str += '        <tbody>';
            str += '            <tr>';
            str += '            <th scope="row">주소</th>';
            str += `                <td>${hospitalInfo.hospitalAddress}</td>`;
            str += '            <tr>';
            str += '            <tr>';
            str += '            <th scope="row">전화번호</th>';
            str += `                <td>${hospitalInfo.hospitalTell}</td>`;
            str += '            <tr>';
            str += '            <tr>';
            str += '            <th scope="row">우편번호</th>';
            str += `                <td>${hospitalInfo.hospitalPost}</td>`;
            str += '            <tr>';

            let str2 = '';
            str2 += `<h2>${hospitalInfo.hospitalName}</h2>`

            document.querySelector('.modal-body').innerHTML = str;
            document.querySelector('#exampleModalLabel').innerHTML = str2;
            $("#exampleModal").modal("show");

            $(document).ready(function () {
                // 모달이 나타날 때 이벤트 감지
                $('#exampleModal').on('shown.bs.modal', function () {
                    // 모달이 나타난 후에 지도를 다시 그림
                    drawMap(hospitalInfo.hospitalLatitude, hospitalInfo.hospitalLongitude);
                });
                // 모달 창 크기가 변경될 때 이벤트 감지
                $('#exammpleModal').on('resize.bs.modal', function () {
                    // 모달 창 크기가 변경될 때마다 지도를 다시 그림
                    drawMap(hospitalInfo.hospitalLatitude, hospitalInfo.hospitalLongitude);
                });
            });

            function drawMap(latitude, longitude) {
                // 기존에 그려진 지도를 지움
                var mapContainer = document.getElementById('map');
                mapContainer.innerHTML = '';

                // 새로운 지도를 그림
                var map = new kakao.maps.Map(mapContainer, 
                mapOption = {
                    center: new kakao.maps.LatLng(latitude, longitude),
                    level: 4
                });

                var map = new kakao.maps.Map(mapContainer, mapOption);

                var imageSrc = "/images/hospital.png"
                    imageSize = new kakao.maps.Size(64, 69),
                    imageOption = {offset: new kakao.maps.Point(27, 69)};

                var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);
                    markerPosition = new kakao.maps.LatLng(latitude, longitude);

                // 마커를 생성하고 지도에 표시
                var markerPosition = new kakao.maps.LatLng(latitude, longitude);
                var marker = new kakao.maps.Marker({
                    position: markerPosition,
                    image: markerImage
                });
                
                // 마커가 지도 위에 표시되도록 설정
                marker.setMap(map);

                var content = '<div class="customoverlay">' +
                '   <a href="https://map.kakao.com/?q=' + encodeURIComponent(result.hospitalName) + '&target=place" target="_blank">' +
                    `   <span class="title">${result.hospitalName}</span>` +
                    '   </a>' +
                    '</div>';

                var position = new kakao.maps.LatLng(latitude, longitude);

                // 커스텀 오버레이를 생성합니다
                var customOverlay = new kakao.maps.CustomOverlay({
                    map: map,
                    position: position,
                    content: content,
                    yAnchor: 1 
                });

                customOverlay.setMap(map);

                kakao.maps.event.addListener(customOverlay, 'click', function() {
                    map.panTo(position);
                });
                
            }

        },
        error: function (result, status, error) {
            console.log(error)
        }
    });
}