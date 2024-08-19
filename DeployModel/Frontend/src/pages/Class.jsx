//Libarary
import { useParams, Link } from "react-router-dom";
import {
  Layout,
  Card,
  List,
  Button,
  Avatar,
  Modal,
  Form,
  Input,
  TimePicker,
  notification,
  Tooltip,
  Tabs,
  Table,
  Image,
  Upload,
  message,
} from "antd";
import {
  PlusOutlined,
  CheckCircleOutlined,
  CheckCircleTwoTone,
  ExclamationCircleOutlined,
  UploadOutlined,
} from "@ant-design/icons";
import { useEffect, useState } from "react";
import dayjs from "dayjs";
const { Sider } = Layout;
import { DeleteOutlined } from "@ant-design/icons";
//Compoment and api
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import GetDataFromRoute from "../compoment/GetDataFromBackend";
import api from "../api";

//css
import "../styles/Sidebar.css";
import "../styles/Class.css";

function Class() {
  //get idClass from url
  const { idClass } = useParams();

  //get all slots of class from class id
  const [slots, setSlots] = useState([]);

  //Detail Class
  const [classDetail, setClassDetail] = useState({});

  //get all students of class from class id
  const [students, setStudents] = useState([]);

  //get Detail slot from form
  const [subject, setSubject] = useState("");
  const [time_start, setTimeStart] = useState("");
  const [time_end, setTimeEnd] = useState(null);

  //get new student from form
  const [name, setNewStudent] = useState("");
  const [imageStudent, setImageStudent] = useState(null);

  // ================================================= GET DATA ================================================
  useEffect(() => {
    getSlot();
    getClass();
    getStudent();
  }, []);

  //get data Class
  const getClass = async () => {
    const classData = await GetDataFromRoute(`classes/${idClass}/`);
    setClassDetail(classData[0]);
  };

  //get data slots of class
  const getSlot = async () => {
    const slotData = await GetDataFromRoute(`classes/${idClass}/slot/`);
    setSlots(slotData);
  };

  //get data Students of class
  const getStudent = async () => {
    const studentsData = await GetDataFromRoute(`students/${idClass}/`);
    setStudents(studentsData);
  };

  const dataSource =
    students?.map((student) => ({
      name: student.name,
      ID: student.student_id,
      picture: <Image width={128} src={student.image} />,
      key: student.id, // Adjust based on your student object structure
    })) || [];

  //================================================ FORM ================================================

  // Form add new Slot --------------------------------------------------------------------------------
  const [isModalSlotVisible, setIsModalSlotVisible] = useState(false);
  const [formSlot] = Form.useForm();

  //open modal
  const showSlotModal = () => {
    setIsModalSlotVisible(true);
  };

  //turn off modal
  const handleSlotCancel = () => {
    setIsModalSlotVisible(false);
  };

  //get information from form modal
  const handleSlotOk = () => {
    formSlot
      .validateFields()
      .then((values) => {
        formSlot.resetFields();
        handleSubmitSlot();
        setIsModalSlotVisible(false);
      })
      .catch((info) => {
        console.log("Validate Failed:", info);
      });
  };

  //***sent data to backend
  //create new slot
  const handleSubmitSlot = async () => {
    try {
      const res = await api.post(`classes/${idClass}/createSlot`, {
        class_id: idClass,
        subject,
        time_start,
        time_end,
      });
      if (res.status === 201) {
        notification.success({
          message: "Success",
          description: `Slot created successfully!`,
          placement: "topRight",
          duration: 3,
        });
        getSlot();
      }
    } catch (error) {
      notification.error({
        message: "Error",
        description: error.message,
        placement: "topRight",
        duration: 3,
      });
    }
  };

  //Delete slot
  const handleDeleteSlot = async (slotId) => {
    try {
      const res = await api.delete(`deleteSlot/${slotId}/`);
      if (res.status === 204) {
        notification.success({
          message: "Success",
          description: `Class deleted successfully!`,
          placement: "topRight",
          duration: 3,
        });
        getSlot(); // Refresh the list of classes
      }
    } catch (error) {
      notification.error({
        message: "Error",
        description: error.message,
        placement: "topRight",
        duration: 3,
      });
    }
  };

  // Form add new student --------------------------------------------------------------------------------
  const [isModalStudentVisible, setIsModalStudentVisible] = useState(false);
  const [formStudent] = Form.useForm();

  //open modal
  const showStudentModal = () => {
    setIsModalStudentVisible(true);
  };

  //Turn off modal
  const handleStudentCancel = () => {
    setIsModalStudentVisible(false);
  };

  //get information from form modal
  const handleStudentOk = () => {
    formStudent
      .validateFields()
      .then((values) => {
        formStudent.resetFields();
        handleSubmitStudent();
        setIsModalStudentVisible(false);
      })
      .catch((info) => {
        console.log("Validate Failed:", info);
      });
  };

  const handleFileChange = (info) => {
    if (info.fileList.length > 0) {
      setImageStudent(info.fileList[0].originFileObj);
    } else {
      setImageStudent(null);
    }
  };

  //sent data to backend
  const handleSubmitStudent = async () => {
    const email = name
      .replace(/\s/g, "")
      .concat("", students.length + 1)
      .concat("", "@gmail.com");
    const password = "123456";

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("class_id", idClass);
    formData.append("image", imageStudent);

    console.log(imageStudent);

    try {
      const res = await api.post(`addStudent/${idClass}/`, formData);
      if (res.status === 201) {
        notification.success({
          message: "Success",
          description: `Student add successfully!`,
          placement: "topRight",
          duration: 3,
        });
        getStudent();
      }
    } catch (error) {
      notification.error({
        message: "Error",
        description: error.message,
        placement: "topRight",
        duration: 3,
      });
      console.log(error);
    }
  };
  const handleDelete = async (studentId) => {
    try {
      await api.delete(`/students/${idClass}/${studentId}/`);
      notification.success({
        message: "Success",
        description: `Student deleted successfully`,
        placement: "topRight",
        duration: 3,
      });
      getStudent();
      // Refresh the data source after deletion
      // You might need to fetch the updated list of students here
    } catch (error) {
      console.log(error);
      message.error("Failed to delete student");
    }
  };

  //================================================ HTML ================================================

  return (
    <Layout>
      <Sider className="sidebar">
        <Logo />
        <MenuList currnentKey={"class"} />
      </Sider>

      <div className="class-information">
        <Card
          title="Class Information"
          className="class-container"
          bordered={false}
        >
          <p className="class-number">Class name: {classDetail.class_name}</p>
          <p className="class's-slot">Semester: {classDetail.semester}</p>
          <p className="class's-slot">
            Total student: {students.length}
            {students.length === 0 && (
              <Tooltip title="No students available">
                <ExclamationCircleOutlined
                  style={{ color: "red", marginLeft: 8 }}
                />
              </Tooltip>
            )}{" "}
          </p>
        </Card>
        <Tabs defaultActiveKey="1" className="Tabs-container" size="large">
          <Tabs.TabPane tab="Slots" key="1">
            <Card
              style={{
                fontSize: "24px",
              }}
              title="Slots: "
              className="slot-container"
              extra={
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={showSlotModal}
                >
                  Add Slot
                </Button>
              }
            >
              <List
                grid={{ gutter: 16, column: 3 }}
                dataSource={slots}
                renderItem={(slot) => (
                  <List.Item>
                    <Link to={`/classes/${idClass}/slot/${slot.id}`}>
                      <Card hoverable={true} style={{ minWidth: "75px" }}>
                        <List.Item.Meta
                          avatar={
                            slot.status ? (
                              <Avatar
                                icon={
                                  <CheckCircleTwoTone twoToneColor="#0adf08" />
                                }
                              />
                            ) : (
                              <Avatar icon={<CheckCircleOutlined />} />
                            )
                          }
                          title={slot.subject}
                          description={`Time: ${slot.time_start} - ${slot.time_end}`}
                        />
                      </Card>
                    </Link>
                    <Button
                      type="danger"
                      icon={<DeleteOutlined />}
                      onClick={() => handleDeleteSlot(slot.id)}
                      style={{ marginTop: "10px" }}
                    >
                      Delete
                    </Button>
                  </List.Item>
                )}
              />
            </Card>
          </Tabs.TabPane>
          <Tabs.TabPane tab="Students" key="2">
            <Card
              style={{
                fontSize: "24px",
              }}
              title="Student: "
              className="slot-container"
              extra={
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={showStudentModal}
                >
                  Add Student
                </Button>
              }
            >
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
                    render: (text) => (
                      <div style={{ textAlign: "left" }}>{text}</div>
                    ),
                  },
                  {
                    title: "Action",
                    key: "action",
                    render: (text, record) => (
                      <Button
                        type="danger"
                        icon={<DeleteOutlined />}
                        onClick={() => handleDelete(record.ID)}
                      >
                        Delete
                      </Button>
                    ),
                  },
                ]}
                dataSource={dataSource}
              ></Table>
            </Card>
          </Tabs.TabPane>
        </Tabs>
      </div>

      {/* ================================================ Modal ================================================ */}
      <Modal
        title="Add new student"
        open={isModalStudentVisible}
        onOk={handleStudentOk}
        onCancel={handleStudentCancel}
      >
        <Form form={formStudent} layout="vertical" name="add_Student_form">
          <Form.Item
            name="Student's name"
            label="Name"
            rules={[
              { required: true, message: "Please input Student's name!" },
            ]}
          >
            <Input
              onChange={(e) => {
                setNewStudent(e.target.value);
              }}
            />
          </Form.Item>
          <Form.Item
            name="Student's image"
            label="Student's image"
            rules={[
              { required: true, message: "Please input Student's image!" },
            ]}
          >
            <Upload
              beforeUpload={() => false} // Prevent automatic upload
              onChange={handleFileChange}
              maxCount={1}
            >
              <Button icon={<UploadOutlined />}>Select File</Button>
            </Upload>
          </Form.Item>
        </Form>
      </Modal>
      <Modal
        title="Add New Slot"
        open={isModalSlotVisible}
        onOk={handleSlotOk}
        onCancel={handleSlotCancel}
      >
        <Form form={formSlot} layout="vertical" name="add_class_form">
          <Form.Item
            name="subject"
            label="Subject"
            rules={[{ required: true, message: "Please input the subject!" }]}
          >
            <Input
              onChange={(e) => {
                setSubject(e.target.value);
              }}
            />
          </Form.Item>
          <Form.Item
            name="time"
            label="Time"
            rules={[{ required: true, message: "Please input the time!" }]}
          >
            <TimePicker.RangePicker
              style={{
                width: "100%",
              }}
              format="HH:mm"
              onChange={(e) => {
                setTimeStart(e[0].format("HH:mm"));
                setTimeEnd(e[1].format("HH:mm"));
              }}
              initialValues={[dayjs("00:00", "HH:mm"), dayjs("00:00", "HH:mm")]}
            />
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  );
}

export default Class;
