//import from libarary
import React, { useState, useEffect, useRef } from "react";
import {
  Layout,
  Card,
  Table,
  Tabs,
  Image,
  Row,
  Col,
  Typography,
  Button,
  Tooltip,
  Progress,
  Select,
  notification,
  message,
} from "antd";

const { Text } = Typography;
const { TabPane } = Tabs;
import {
  PlusOutlined,
  ClockCircleTwoTone,
  CheckCircleOutlined,
  CheckCircleTwoTone,
  ExclamationCircleOutlined,
} from "@ant-design/icons";
import { useParams } from "react-router-dom";
const { Sider } = Layout;
import dayjs from "dayjs";

//import from src
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import GetDataFromRoute from "../compoment/GetDataFromBackend";
import CameraCapture from "../compoment/CameraCapture";

//CSS
import "../styles/Attendent.css";
import "../styles/Sidebar.css";
import api from "../api";

function Attendent() {
  let params = useParams();
  const [className, setClassName] = useState("");
  const [students, setStudents] = useState([]);
  const [slotInfomation, setSlotInfomation] = useState([]);
  const [timeFrames, setTimeFrame] = useState([]);
  const [studentsInOneFrame, setStudentsInOneFrame] = useState([]);

  const [duration, setDuration] = useState(["", 0]);
  const [indexTimeFrame, setIndexTimeFrame] = useState(0);
  const [isCaturing, setIsCapturing] = useState(false);
  const cameraRef = useRef(null);

  const [isRunning, setIsRunning] = useState(false);
  const [time, setTime] = useState(0);

  // ======================================= get data =======================================
  useEffect(() => {
    getClass();
    getSlot();
    getStudent();
    getTimeFrame();
  }, []);

  // ===================================================== TIMER =====================================================
  useEffect(() => {
    let interval;

    if (isRunning && time > 0) {
      interval = setInterval(() => {
        setTime((prevTime) => {
          if (prevTime <= 1000) {
            clearInterval(interval);
            setIsRunning(false);
            return 0;
          }
          return prevTime - 1000;
        });
      }, 1000); // Update time every second
    }

    if (
      (duration[1] - time) / 1000 ==
        Math.floor(((duration[1] / 15) * indexTimeFrame) / 1000) &&
      indexTimeFrame <= 15 &&
      isRunning &&
      timeFrames.length < 15
    ) {
      captureImage();
      setIndexTimeFrame(indexTimeFrame + 1);
    } else if (indexTimeFrame >= 15 || timeFrames.length >= 15) {
      stopCamera();
      setIndexTimeFrame(indexTimeFrame + 1);
    }

    console.log(
      "time: ",
      duration[1] - time,
      "   mock: ",
      Math.floor((duration[1] / 15) * indexTimeFrame)
    );

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, [isRunning, time]);

  const setTimer = () => {
    const milliseconds = duration[1]; // Convert minutes to milliseconds
    setTime(milliseconds);
  };

  const formatTime = (time) => {
    const seconds = `0${Math.floor((time / 1000) % 60)}`.slice(-2);
    const minutes = `0${Math.floor((time / 60000) % 60)}`.slice(-2);
    const hours = `0${Math.floor(time / 3600000)}`.slice(-2);

    return `${hours}:${minutes}:${seconds}`;
  };

  // ===================================================== GET DATA =====================================================
  const getClass = async () => {
    const classData = await GetDataFromRoute(`classes/${params.idClass}/`);
    setClassName(classData[0].class_name);
  };

  const getSlot = async () => {
    const slotData = await GetDataFromRoute(`slot${params.idSlot}/`);
    setSlotInfomation(slotData[0]);
    const durationData = dayjs(slotData[0].time_end, "HH:mm:ss").diff(
      dayjs(slotData[0].time_start, "HH:mm:ss")
    );

    const hours = Math.floor(durationData / 3600000);
    const minutes = Math.floor((durationData % 3600000) / 60000);

    setDuration([
      `${String(hours).padStart(2, "0")}h${String(minutes).padStart(2, "0")}p`,
      durationData,
    ]);
  };

  const getStudent = async () => {
    const studentsData = await GetDataFromRoute(
      `addStudent/${params.idClass}/`
    );
    setStudents(studentsData);
  };

  const getTimeFrame = async () => {
    const timeFrameData = await GetDataFromRoute(
      `slot${params.idSlot}/timeFrame/`
    );
    setTimeFrame(timeFrameData);
  };

  // ============= data source =============
  const dataSource =
    students?.map((student) => ({
      name: student.name,
      ID: student.id,
      picture: <Image width={200} src={student.image} />, // Adjust based on your student object structure
    })) || [];
  const dataSourceAtOneFrame =
    studentsInOneFrame?.map((student) => ({
      name: student.name,
      ID: student.id,
      picture: 1,
      //picture: <Image width={128} src={student.image} />, // Adjust based on your student object structure
    })) || [];

  const tableStudent = (dataSource) => {
    return (
      <>
        <Table
          columns={[
            {
              title: "Name",
              dataIndex: "name",
              key: "name",
              render: (image) => (
                <div style={{ fontSize: "15px" }}>{image}</div>
              ),
            },
            {
              title: "ID",
              dataIndex: "ID",
              key: "ID",
            },
            {
              title: "Picture",
              dataIndex: "picture",
              key: "picture",
              render: (image) => (
                <div style={{ textAlign: "left" }}>{image}</div>
              ),
            },
            {
              title: "Attend status",
            },
          ]}
          dataSource={dataSource}
        ></Table>
      </>
    );
  };

  // ============= handle click =============
  const handleTabClick = async (key) => {
    console.log(key);

    if (key != 0) {
      const data = await GetDataFromRoute(`timeFrame${key}/`);
      const studentIds = data.map((item) => item.student_id);

      setStudentsInOneFrame(
        students.filter((student) => studentIds.includes(student.id))
      );
      console.log(studentsInOneFrame);
    }
  };

  const handleClockClick = async () => {
    setIsRunning(!isRunning);
    if (isRunning) {
      stopCamera();
      setIndexTimeFrame(0);
    } else {
      startCamera();
    }
    setTimer();
  };

  // ======================================= progress bar =======================================
  const progressPercent =
    duration[1] > 0 ? 100 - (time / duration[1]) * 100 : 0;

  // ====================================================== Camera ======================================================
  const [devices, setDevices] = useState([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

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
      formData.append("slot_id", slotInfomation.id);

      const res = await api.post(
        `slot${slotInfomation.id}/timeFrame/`,
        formData
      );
      if (res.status === 201) {
        message.info(`Timeframe add successfully!`);
        getTimeFrame();
      }
    });
  };

  const options = devices.map((device, index) => ({
    value: device.deviceId,
    label: device.label || `Camera ${index + 1}`,
  }));

  // ====================================================== Return ======================================================
  return (
    <Layout>
      <Sider className="sidebar">
        <Logo />
        <MenuList currnentKey={"activity"} />
      </Sider>
      <div className="attendent-information">
        <Row style={{ width: "100%", justifyContent: "center" }}>
          <Col>
            <Card
              title="Slot Information"
              className="class-container"
              bordered={false}
              style={{ minWidth: "500px", paddingBottom: "0px" }}
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
              <Row>
                <Col span={8}>
                  <Text strong>Subject:</Text>
                </Col>
                <Col span={16}>
                  <Text>{slotInfomation.subject}</Text>
                </Col>
              </Row>

              <Row style={{ marginTop: "10px" }}>
                <Col span={8}>
                  <Text strong>Class:</Text>
                </Col>
                <Col span={16}>
                  <Text>{className}</Text>
                </Col>
              </Row>

              <Row style={{ marginTop: "10px" }}>
                <Col span={8}>
                  <Text strong>Date:</Text>
                </Col>
                <Col span={16}>
                  <Text>
                    {dayjs(slotInfomation.time_start, "HH:mm:ss").format(
                      "HH:mm A"
                    )}{" "}
                    -{" "}
                    {dayjs(slotInfomation.time_end, "HH:mm:ss").format(
                      "HH:mm A"
                    )}
                  </Text>
                </Col>
              </Row>

              <Row style={{ marginTop: "10px" }}>
                <Col span={8}>
                  <Text strong>Duration:</Text>
                </Col>
                <Col span={16}>
                  <Text>{duration[0]}</Text>
                </Col>
              </Row>
              <Row style={{ marginTop: "10px" }}>
                <Col span={8} style={{ margin: "auto" }}>
                  <Text>Time: {formatTime(time)}</Text>
                </Col>
                <Col span={16}>
                  <Progress
                    percent={progressPercent}
                    strokeColor="rgb(24, 144, 255)"
                    style={{ marginTop: "10px", marginBottom: "10px" }}
                    showInfo={false}
                  />
                </Col>
              </Row>
            </Card>
          </Col>
          <Col>
            <Card
              title="Camera"
              style={{ width: "95%", margin: "10px", padding: "10px" }}
            >
              <Row style={{ width: "100%", justifyContent: "center" }}>
                <video
                  ref={videoRef == null ? imageSrc : videoRef}
                  autoPlay
                  width="300"
                  height="200"
                  style={{
                    border: "1px solid ",
                    borderRadius: "5px",
                    margin: "10px",
                  }}
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
          </Col>
        </Row>
        <Tabs
          defaultActiveKey="1"
          className="Tabs-container"
          size="large"
          onTabClick={handleTabClick}
        >
          <Tabs.TabPane tab={"All student"} key={0}>
            {tableStudent(dataSource)}
          </Tabs.TabPane>
          {timeFrames?.map((eachTimeFrame, index) => (
            <Tabs.TabPane tab={index + 1} key={eachTimeFrame.id}>
              {tableStudent(dataSourceAtOneFrame)}
              <Card title="Total review" style={{ margin: "10px" }}>
                <Image src={timeFrames[index].embedding} />
              </Card>
            </Tabs.TabPane>
          ))}
        </Tabs>
      </div>
    </Layout>
  );
}

export default Attendent;
