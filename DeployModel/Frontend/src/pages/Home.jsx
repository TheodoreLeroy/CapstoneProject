// libarary
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Layout,
  Card,
  List,
  Button,
  Avatar,
  Modal,
  Form,
  Input,
  message,
  notification,
} from "antd";
import { PlusOutlined, BookTwoTone } from "@ant-design/icons";
const { Content, Footer, Sider } = Layout;

//compoment
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import GetDataFromRoute from "../compoment/GetDataFromBackend";
import api from "../api";

// css files
import "../styles/Home.css";
import "../styles/Sidebar.css";

function Home() {
  //Classes
  const [classes, setClasses] = useState([]);

  //new class
  const [class_name, setClassName] = useState("");
  const [semester, setSemester] = useState("");

  // ======================================= get data =======================================
  useEffect(() => {
    getClass();
  }, []);

  //get classes data which also contain id
  const getClass = async () => {
    const classData = await GetDataFromRoute(`classes/detail`);
    setClasses(classData);
  };

  //to navigate to another page
  const navigate = useNavigate();

  //======================================= Form =======================================
  const [form] = Form.useForm();

  //form add new class
  const [isModalVisible, setIsModalVisible] = useState(false);

  //open modal
  const showModal = () => {
    setIsModalVisible(true);
  };

  //turn off modal
  const handleCancel = () => {
    setIsModalVisible(false);
  };

  //get information from form modal
  const handleOk = () => {
    form
      .validateFields()
      .then((values) => {
        form.resetFields();
        console.log(class_name, semester);

        handleClassSubmit();
        setIsModalVisible(false);
      })
      .catch((info) => {
        console.log("Validate Failed:", info);
      });
  };

  //sent data to backend
  //url: addClass/ - data: class_name, semester
  const handleClassSubmit = async () => {
    try {
      const res = await api.post("addClass/", { class_name, semester });
      if (res.status === 201) {
        notification.success({
          message: "Success",
          description: `Class created successfully!`,
          placement: "topRight",
          duration: 3,
        });
        getClass();
      }
    } catch (Error) {
      notification.error({
        message: "Error",
        description: Error.response.data.class_name,
        duration: 3,
      });
    }
  };
  //delete class data
  const handleDeleteClass = async (classId) => {
    try {
      const res = await api.delete(`deleteClass/${classId}/`);
      if (res.status === 204) {
        notification.success({
          message: "Success",
          description: `Class deleted successfully!`,
          placement: "topRight",
          duration: 3,
        });
        getClass(); // Refresh the list of classes
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

  return (
    <Layout>
      <Sider className="sidebar">
        <Logo />
        <MenuList currnentKey={"home"} />
      </Sider>
      <Layout style={{ minHeight: "100vh" }}>
        <Layout className="site-layout">
          <Content style={{ margin: "0 16px" }}>
            <div
              className="site-layout-background"
              style={{ padding: 24, minHeight: 360 }}
            >
              <Card
                title="Classes"
                extra={
                  <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={showModal}
                  >
                    Add Class
                  </Button>
                }
              >
                <List
                  itemLayout="horizontal"
                  dataSource={classes}
                  renderItem={(classDetail) => (
                    <List.Item
                      actions={[
                        <Button
                          type="link"
                          onClick={(e) =>
                            navigate(`/classes/${classDetail.id}`)
                          }
                        >
                          View
                        </Button>,
                        <Button
                          type="link"
                          danger
                          onClick={() => handleDeleteClass(classDetail.id)}
                        >
                          Delete
                        </Button>,
                      ]}
                    >
                      <List.Item.Meta
                        avatar={
                          <Avatar
                            style={{ backgroundColor: "#6DAAFF" }}
                            icon={<BookTwoTone />}
                          />
                        }
                        title={classDetail.class_name}
                        description={`Semester: ${classDetail.semester}`}
                      />
                    </List.Item>
                  )}
                />
              </Card>
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>
            Attendance System ©2024 Created by YourName
          </Footer>
        </Layout>

        <Modal
          title="Add New Class"
          open={isModalVisible}
          onOk={handleOk}
          onCancel={handleCancel}
        >
          <Form
            form={form}
            layout="vertical"
            name="add_class_form"
            requiredMark="optional"
          >
            <Form.Item
              name="name"
              label="Class Name"
              rules={[
                { required: true, message: "Please input the class name!" },
              ]}
            >
              <Input onChange={(e) => setClassName(e.target.defaultValue)} />
            </Form.Item>
            <Form.Item
              name="semester"
              label="Semester"
              rules={[
                { required: true, message: "Please input the Semester!" },
              ]}
            >
              <Input onChange={(e) => setSemester(e.target.defaultValue)} />
            </Form.Item>
          </Form>
        </Modal>
      </Layout>
    </Layout>
  );
}

export default Home;
