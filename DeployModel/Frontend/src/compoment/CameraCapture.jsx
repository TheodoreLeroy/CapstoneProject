import { useState, useRef, useEffect } from "react";

import { Card, Tooltip, Button, Select, Row, Col, notification } from "antd";
import { ClockCircleTwoTone, VideoCameraOutlined } from "@ant-design/icons";

import api from "../api";

export default function CameraCapture({ idSlot, isRunning }) {
  const [devices, setDevices] = useState([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null); // To keep track of the stream

  useEffect(() => {
    const getDevices = async () => {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(
        (device) => device.kind === "videoinput"
      );
      setDevices(videoDevices);
      setSelectedDeviceId(videoDevices[0]?.deviceId); // Default to the first camera
    };
    getDevices();
  }, []);

  useEffect(() => {
    if (!isRunning) {
      stopCamera();
    } else {
      startCamera();
    }
  }, [isRunning]);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: selectedDeviceId ? { exact: selectedDeviceId } : undefined,
      },
    });
    videoRef.current.srcObject = stream;
    streamRef.current = stream; // Store the stream in a ref
  };

  const stopCamera = () => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    videoRef.current.srcObject = null;
  };

  const captureImage = () => {
    const context = canvasRef.current.getContext("2d");
    context.drawImage(
      videoRef.current,
      0,
      0,
      canvasRef.current.width,
      canvasRef.current.height
    );

    // Convert the canvas to a Blob (image file)
    canvasRef.current.toBlob(async (blob) => {
      const file = new File([blob], "capture.png", { type: "image/png" });

      // Prepare form data
      const formData = new FormData();
      formData.append("embedding", file);
      formData.append("slot_id", idSlot);

      const res = await api.post(`slot${idSlot}/timeFrame/`, formData);
      if (res.status === 201) {
        notification.success({
          message: "Success",
          description: `Timeframe add successfully!`,
          placement: "topRight",
          duration: 3,
        });
        // getStudent();
      }
    });
  };

  const handleClockClick = () => {
    if (isRunning) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  const options = devices.map((device, index) => ({
    value: device.deviceId,
    label: device.label || `Camera ${index + 1}`,
  }));

  return (
    <Card
      title="Camera"
      style={{ width: "95%", margin: "10px", padding: "10px" }}
      extra={
        <Tooltip title={!isRunning ? "Start slot" : "End slot"}>
          <Button
            type="primary"
            icon={
              <ClockCircleTwoTone
                twoToneColor={!isRunning ? "#1677ff" : "#0ADF08"}
              />
            }
            shape="circle"
            onClick={handleClockClick}
            style={
              !isRunning
                ? { backgroundColor: "#1677ff" }
                : { backgroundColor: "#0ADF08" }
            }
          ></Button>
        </Tooltip>
      }
    >
      <Row style={{ width: "100%", justifyContent: "center" }}>
        <video
          ref={videoRef == null ? imageSrc : videoRef}
          autoPlay
          width="300"
          height="200"
          style={{ border: "1px solid ", borderRadius: "5px", margin: "10px" }}
        ></video>
      </Row>
      <Row style={{ width: "100%" }}>
        <Col>
          <Select
            value={selectedDeviceId}
            onChange={(value) => setSelectedDeviceId(value)}
            options={options}
            style={{ width: 200 }} // Adjust the width as needed
            placeholder="Select a camera"
          />
        </Col>
        <Col>
          <Button onClick={captureImage}>take picture</Button>
        </Col>
      </Row>
      <canvas
        ref={canvasRef}
        style={{ display: "none" }}
        width="300"
        height="200"
      ></canvas>
    </Card>
  );
}
