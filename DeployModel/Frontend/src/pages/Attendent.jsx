//import from libarary
import React, { useState, useEffect } from 'react';
import { Layout, Card, Table, Tabs, Image } from 'antd';
const { TabPane } = Tabs;
import { PlusOutlined, CheckCircleOutlined, CheckCircleTwoTone, ExclamationCircleOutlined } from '@ant-design/icons';
import { useParams } from "react-router-dom";
const { Sider } = Layout;
import dayjs from 'dayjs';

//import from src
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import GetDataFromRoute from '../compoment/GetDataFromBackend';
import ProgressBar from '../compoment/ProgressBar';

//CSS
import "../styles/Attendent.css";
import "../styles/Sidebar.css";

function Attendent() {
    let params = useParams();
    const [className, setClassName] = useState("");
    const [students, setStudents] = useState([]);
    const [slotInfomation, setSlotInfomation] = useState([]);
    const [timeFrames, setTimeFrame] = useState([]);
    const [studentsInOneFrame, setStudentsInOneFrame] = useState([]);

    const [duration, setDuration] = useState(0);

    const [isRunning, setIsRunning] = useState(0);

    // ======================================= get data =======================================
    useEffect(() => {
        getClass();
        getSlot();
        getStudent();
        getTimeFrame();

    }, [])

    const getClass = async () => {
        const classData = await GetDataFromRoute(`class${params.idClass}/`);
        setClassName(classData[0].class_name);
    }

    const getSlot = async () => {
        const slotData = await GetDataFromRoute(`slot${params.idSlot}/`);
        setSlotInfomation(slotData[0]);
        setDuration(dayjs(slotInfomation.time_end, 'HH:mm:ss').diff(dayjs(slotInfomation.time_start, 'HH:mm:ss')));
    }

    const getStudent = async () => {
        const studentsData = await GetDataFromRoute(`studentsClass${params.idClass}/`);
        setStudents(studentsData);
    }

    const getTimeFrame = async () => {
        const timeFrameData = await GetDataFromRoute(`slot${params.idSlot}/timeFrame/`);
        setTimeFrame(timeFrameData);
        console.log(timeFrameData);
    }
    
    
 
    const dataSource = students?.map(student => ({
        name: student.name,
        ID: student.id,
        picture: 1,
        picture: <Image
            width={200}
            src={student.image}
        />, // Adjust based on your student object structure
    })) || [];
    const dataSourceAtOneFrame = studentsInOneFrame?.map(student => ({
        name: student.name,
        ID: student.id,
        picture: 1,
        picture: <Image
            width={200}
            src={student.image}
        />, // Adjust based on your student object structure
    })) || [];

    const tableStudent = (dataSource) => {
        return <Table
            columns={[
                {
                    title: 'Name',
                    dataIndex: 'name',
                    key: 'name',
                    render: (image) => <div style={{ fontSize: "15px" }}>{image}</div>,
                },
                {
                    title: 'ID',
                    dataIndex: 'ID',
                    key: 'ID',
                },
                {
                    title: 'Picture',
                    dataIndex: 'picture',
                    key: 'picture',
                    render: (image) => <div style={{ textAlign: 'center' }}>{image}</div>,
                },
            ]}
            dataSource={dataSource}
        ></Table>
    }
    const handleTabClick = async (key) => {
        console.log(key);
        
        if (key != 0){
            const data = await GetDataFromRoute(`timeFrame${key}/`);
            const studentIds = data.map(item => item.student_id);
            
            setStudentsInOneFrame(students.filter(student => studentIds.includes(student.id)))
            console.log(studentsInOneFrame);
        }
    };

    return <Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList currnentKey={'activity'} />
        </Sider>
        <div className="attendent-information">
            <Card
                title="Slot Information"
                className="class-container"
                bordered={false}
            >
                <p className="slot-name">Subject: {slotInfomation.subject}</p>
                <p className="slot-class">Class: {className} </p>
                <p className="slot-date">Date: {slotInfomation.time_start} - {slotInfomation.time_end}</p>
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
}

export default Attendent