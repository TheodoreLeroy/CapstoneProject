//import from libarary
import React, { useState, useEffect } from "react";
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

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, [isRunning, time]);

  const startPause = () => {
    if (time > 0) {
      setIsRunning(!isRunning);
    }
  };

  // nope
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
    console.log(timeFrameData);
  };

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
      //   picture: 1,
      picture: <Image width={128} src={student.image} />, // Adjust based on your student object structure
    })) || [];

  const tableStudent = (dataSource) => {
    return (
      <Table
        columns={[
          {
            title: "Name",
            dataIndex: "name",
            key: "name",
            render: (image) => <div style={{ fontSize: "15px" }}>{image}</div>,
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
            render: (image) => <div style={{ textAlign: "left" }}>{image}</div>,
          },
          {
            title: "Attend status",
          },
        ]}
        dataSource={dataSource}
      ></Table>
    );
  };
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
    setTimer();
    try {
      const response = await api.post("slot/camera/", {});
      notification.success({
        message: "Success",
        description: response.data.status,
        placement: "topRight",
        duration: 3,
      });
    } catch (error) {
      notification.error({
        message: "Error",
        description: error.message,
        placement: "topRight",
        duration: 3,
      });
    }
  };

  const progressPercent =
    duration[1] > 0 ? 100 - (time / duration[1]) * 100 : 0;

  return (
    <Layout>
      <Sider className="sidebar">
        <Logo />
        <MenuList currnentKey={"activity"} />
      </Sider>
      <div className="attendent-information">
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
                {dayjs(slotInfomation.time_start, "HH:mm:ss").format("HH:mm A")}{" "}
                - {dayjs(slotInfomation.time_end, "HH:mm:ss").format("HH:mm A")}
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
            </Tabs.TabPane>
          ))}
        </Tabs>
      </div>
    </Layout>
  );
}

export default Attendent;
