import React, { useState } from 'react';
import { Layout, Menu, Breadcrumb, Card, List, Button, Avatar, Calendar, Row, Col, Modal, Form, Input, message } from 'antd';
import { PlusOutlined, EditOutlined, CheckCircleOutlined } from '@ant-design/icons';

const { Header, Content, Footer, Sider } = Layout;

const HomePage = () => {
    const [classes, setClasses] = useState([
        { name: 'Math 101', teacher: 'Mr. Smith' },
        { name: 'Biology 202', teacher: 'Ms. Johnson' },
        // More classes...
    ]);

    const [isModalVisible, setIsModalVisible] = useState(false);
    const [form] = Form.useForm();

    const showModal = () => {
        setIsModalVisible(true);
    };

    const handleOk = () => {
        form
            .validateFields()
            .then(values => {
                form.resetFields();
                setClasses([...classes, values]);
                setIsModalVisible(false);
                message.success('Class added successfully!');
            })
            .catch(info => {
                console.log('Validate Failed:', info);
            });
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Layout className="site-layout">
                <Content style={{ margin: '0 16px' }}>
                    <Breadcrumb style={{ margin: '16px 0' }}>
                        <Breadcrumb.Item>Home</Breadcrumb.Item>
                    </Breadcrumb>
                    <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
                        <Row gutter={16}>
                            <Col span={12}>
                                <Card title="Classes" extra={<Button type="primary" icon={<PlusOutlined />} onClick={showModal}>Add Class</Button>}>
                                    <List
                                        itemLayout="horizontal"
                                        dataSource={classes}
                                        renderItem={item => (
                                            <List.Item
                                                actions={[<Button type="link">View</Button>, <Button type="link">Edit</Button>]}
                                            >
                                                <List.Item.Meta
                                                    avatar={<Avatar icon={<CheckCircleOutlined />} />}
                                                    title={item.name}
                                                    description={`Teacher: ${item.teacher}`}
                                                />
                                            </List.Item>
                                        )}
                                    />
                                </Card>
                            </Col>
                            <Col span={12}>
                                <Card title="Upcoming Classes">
                                    <Calendar fullscreen={false} />
                                </Card>
                            </Col>
                        </Row>
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>Attendance System ©2024 Created by YourName</Footer>
            </Layout>

            <Modal
                title="Add New Class"
                visible={isModalVisible}
                onOk={handleOk}
                onCancel={handleCancel}
            >
                <Form form={form} layout="vertical" name="add_class_form">
                    <Form.Item
                        name="name"
                        label="Class Name"
                        rules={[{ required: true, message: 'Please input the class name!' }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="teacher"
                        label="Teacher's Name"
                        rules={[{ required: true, message: 'Please input the teacher\'s name!' }]}
                    >
                        <Input />
                    </Form.Item>
                    {/* Add more fields as needed */}
                </Form>
            </Modal>
        </Layout>
    );
};

export default HomePage;
