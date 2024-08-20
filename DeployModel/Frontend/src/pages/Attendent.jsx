//import from libarary
import { ClockCircleTwoTone, CheckCircleOutlined } from "@ant-design/icons";
import {
  Button,
  Card,
  Checkbox,
  Col,
  Image,
  Layout,
  Progress,
  Row,
  Select,
  Table,
  Tabs,
  Tooltip,
  Typography,
  message,
} from "antd";
import dayjs from "dayjs";
import React, { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";

const { Text } = Typography;
const { Sider } = Layout;

//import from src
import GetDataFromRoute from "../compoment/GetDataFromBackend";
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";

//CSS
import api from "../api";
import "../styles/Attendent.css";
import "../styles/Sidebar.css";

function Attendent() {
  let params = useParams();
  const [className, setClassName] = useState("");
  const [students, setStudents] = useState([]);
  const [slotInfomation, setSlotInfomation] = useState([]);
  const [timeFrames, setTimeFrame] = useState([]);
  const [studentsInOneFrame, setStudentsInOneFrame] = useState([]);
  const [log, setLog] = useState([]);

  const [isChangingStatus, setIsChangingStatus] = useState(false);

  const [duration, setDuration] = useState(["", 0]);
  const [indexTimeFrame, setIndexTimeFrame] = useState(0);

  const [isRunning, setIsRunning] = useState(false);
  const [time, setTime] = useState(0);

  // ===================================================== get data =====================================================
  useEffect(() => {
    getClass();
    getSlot();
    getStudent();
    getTimeFrame();
    getLog();
  }, []);

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

  const getLog = async () => {
    const logData = await GetDataFromRoute(
      `log${params.idSlot}/`
    );
    setLog(logData);
  };

  // ====================================================== progress bar ======================================================
  const progressPercent =
    (!(duration[1] > 0) || isRunning) ? 100 - (time / duration[1]) * 100 : 0;
  console.log(progressPercent);


  // ===================================================== TIMER =====================================================
  useEffect(() => {
    let interval;

    if (isRunning && time > 0 && timeFrames.length < 15) {
      interval = setInterval(() => {
        setTime((prevTime) => {
          if (prevTime <= 1000) {
            clearInterval(interval);
            setIsRunning(false);
            return 0;
          }
          console.log("time: ", duration[1] - time, "Next time: ", Math.floor(((duration[1] / 15) * indexTimeFrame) / 1000));

          return prevTime - 1000;
        });
      }, 1000); // Update time every second
    } else if (timeFrames.length <= 15) {
      setTime(0)
      stopCamera()
    }

    if (
      ((duration[1] - time) / 1000 ==
        Math.floor(((duration[1] / 15) * indexTimeFrame) / 1000) &&
        indexTimeFrame <= 15 &&
        isRunning &&
        timeFrames.length < 15 &&
        (duration[1] - time) / 1000 != 0) ||
      (duration[1] - time) / 1000 == 1
    ) {
      captureImage();
      setIndexTimeFrame(indexTimeFrame + 1);
    } else if (indexTimeFrame >= 15 || timeFrames.length >= 15) {
      stopCamera();
      getLog();
      setIndexTimeFrame(indexTimeFrame + 1);
    }

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


  // ====================================================== handle click ======================================================
  const handleTabClick = async (key) => {
    console.log("Key: ", key);

    if (key != 0) {
      const data = await GetDataFromRoute(`timeFrame${key}/`);
      const studentIds = data.map((item) => item.student_id);

      setStudentsInOneFrame(
        students.filter((student) => studentIds.includes(student.student_id))
      );
    }
  };

  const handleClockClick = async () => {
    setIsRunning(!isRunning);
    if (isRunning) {
      setIndexTimeFrame(0);
    }
    setTimer();
  };

  const handleStatusClick = async () => {
    if (!isChangingStatus) {
      setIsChangingStatus(!isChangingStatus);
    }
    console.log(isChangingStatus);
  };

  const handleSaveButton = async () => {
    setIsChangingStatus(!isChangingStatus);
    console.log(isChangingStatus);
  };

  // ====================================================== data source ======================================================

  const attendStatusRender = (student) => {
    if (log.length == 0) {
      return <p style={{ color: "red" }}> not yet </p>
    }
    const status = log.find(log => log.student_id === student.student_id);
    if (!isChangingStatus) {
      return status.attend_status ? <p style={{ color: "green" }}> attendent </p> : <p style={{ color: "red" }}> absent </p>
    } else {
      return <Checkbox defaultChecked={status.attend_status} onClick={handleStatusClick}>Attendent</Checkbox>
    }

  }
  const dataSource =
    students?.map((student) => ({
      name: student.name,
      ID: student.student_id,
      picture: <Image width={200} src={student.image} />, // Adjust based on your student object structure
      attendStatusData: (attendStatusRender(student)),
    })) || [];
  const dataSourceAtOneFrame =
    studentsInOneFrame?.map((student) => ({
      name: student.name,
      ID: student.student_id,
      picture: <Image width={200} src={student.image} />,
      attendStatus: "attentdent",
    })) || [];



  const tableAllStudent = () => {
    return (
      <>
        <Table
          columns={[
            {
              title: "Name",
              dataIndex: "name",
              key: "name",
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
                <div style={{ textAlign: "center" }}>{image}</div>
              ),
            },
            {
              title: "Attend status",
              dataIndex: "attendStatusData",
              key: "attendStatusData",
            },
          ]}
          dataSource={dataSource}
        ></Table>
      </>
    );
  };
  const tableStudent = () => {
    return (
      <>
        <Table
          columns={[
            {
              title: "Name",
              dataIndex: "name",
              key: "name",
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
                <div style={{ textAlign: "center" }}>{image}</div>
              ),
            },
          ]}
          dataSource={dataSourceAtOneFrame}
        ></Table>
      </>
    );
  };



  // ====================================================== Camera ======================================================
  const [devices, setDevices] = useState([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState(null);
  const [imageSrc] = useState(null);
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
    startCamera();
  }, []);

  useEffect(() => {
    stopCamera();
    startCamera();
  }, [selectedDeviceId])

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

  const siderStyle = {
    overflow: "auto",
    height: "100vh",
    position: "fixed",
    insetInlineStart: 0,
    top: 0,
    bottom: 0,
    scrollbarWidth: "thin",
    scrollbarColor: "unset",
  };

  // ====================================================== Return ======================================================
  return (
    <Layout hasSider>
      {/* ====================================================== Sider ====================================================== */}
      <Sider className="sidebar" style={siderStyle}>
        <Logo />
        <MenuList currnentKey={"activity"} />
      </Sider>
      {/* ====================================================== MAIN ====================================================== */}
      <Layout
        className="attendent-information"
        style={{
          marginInlineStart: 200,
        }}
      >
        {/* ====================================================== Slot Information ====================================================== */}
        <Row style={{ width: "100%", justifyContent: "center" }}>
          <Col>
            <Card
              title="Slot Information"
              className="class-container"
              bordered={false}
              style={{ minWidth: "500px", paddingBottom: "0px" }}
              extra={
                <Tooltip title={timeFrames.length >= 15
                  ? "Enought time frames" : !isRunning ? "Start slot" : "End slot"}>
                  <Button
                    disabled={timeFrames.length >= 15}
                    type="primary"
                    icon={timeFrames.length >= 15 ?
                      <CheckCircleOutlined /> :
                      <ClockCircleTwoTone />

                    }
                    shape="circle"
                    onClick={handleClockClick}
                    style={
                      timeFrames.length >= 15
                        ? { backgroundColor: "#0ADF08", borderColor: "#0ADF08" }
                        : !isRunning
                          ? { backgroundColor: "#1677ff", borderColor: "#1677ff" }
                          : { backgroundColor: "#0ADF08", borderColor: "#0ADF08" }
                    }
                  ></Button>
                </Tooltip>
              }
            >
              {/* infomation */}
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
                      "HH:mm"
                    )}{" "}
                    -{" "}
                    {dayjs(slotInfomation.time_end, "HH:mm:ss").format(
                      "HH:mm"
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
                    style={{ marginTop: "10px", marginBottom: "10px" }}
                    showInfo={false}
                  />
                </Col>
              </Row>
            </Card>
          </Col>
          <Col>
            {/* ====================================================== camera ====================================================== */}
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
              <Row style={{ width: "100%", justifyContent: "center" }}>
                <Col>
                  <Select
                    value={selectedDeviceId}
                    onChange={(value) => {
                      setSelectedDeviceId(value);
                    }}
                    options={options}
                    style={{ width: 200 }} // Adjust the width as needed
                    placeholder="Select a camera"
                  />
                </Col>
                {/* show button */}
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
          style={{
            minWidth: "750px",
            margin: "auto",
            width: "80%",
          }}
          tabBarExtraContent={
            <Button onClick={handleSaveButton}>{isChangingStatus ? "Save" : "Edit"}</Button>
          }
        >
          <Tabs.TabPane tab={"All student"} key={0}>
            {tableAllStudent(dataSource)}
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
      </Layout>
    </Layout>
  );
}

export default Attendent;
