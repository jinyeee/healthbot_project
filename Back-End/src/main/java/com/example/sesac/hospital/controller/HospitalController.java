package com.example.sesac.hospital.controller;

import com.example.sesac.hospital.dto.HospitalDepReq;
import com.example.sesac.hospital.dto.HospitalDto;
import com.example.sesac.hospital.dto.HospitalReviewSumDto;
import com.example.sesac.hospital.service.HospitalService;
import com.example.sesac.util.QueryStringArgResolver;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("hospital")
@RequiredArgsConstructor
@Slf4j
public class HospitalController {
    private final HospitalService hospitalService;

    @GetMapping("/{hospitalId}")
    public ResponseEntity<HospitalDto> getOneHospital(@PathVariable(name = "hospitalId") Long hospitalId) {
        return new ResponseEntity<>(hospitalService.getHospital(hospitalId), HttpStatus.OK);
    }

    @GetMapping
    public ResponseEntity<List<HospitalDto>> getAllHospitals() {
        return new ResponseEntity<>(hospitalService.getAll(), HttpStatus.OK);
    }

    @GetMapping("/find")
    public ResponseEntity<List<HospitalReviewSumDto>> findAllByDepartment(@QueryStringArgResolver HospitalDepReq hospitalDepReq) {
        return new ResponseEntity<>(hospitalService.getHospitalList(hospitalDepReq), HttpStatus.OK);

    }


}
