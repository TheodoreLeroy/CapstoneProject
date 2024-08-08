//import from libarary
import React, { useState, useEffect } from 'react';
import { Layout, Card, Steps } from 'antd';
import { useParams } from "react-router-dom";
const { Sider } = Layout;

//import from src
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import Slot from "../compoment/Slot";
import GetDataFromRoute from '../compoment/GetDataFromBackend';

//CSS
import "../styles/Attendent.css";
import "../styles/Sidebar.css";

function Attendent() {
    let params = useParams();
    const [classDetail, setClassDetail] = useState({});
    const [students, setStudents] = useState([]);
    const [slotInfomation, setSlotInfomation] = useState([])

    const [current, setCurrent] = useState(0);
    const onChange = (value) => {
        console.log('onChange:', value);
        setCurrent(value);
    };
    const description = 'This is a description.';

    // ======================================= get data =======================================
    useEffect(() => {
        getClass();
        getSlot();
        getStudent();
    }, [])

    const getClass = async () => {
        const classData = await GetDataFromRoute(`class${params.idClass}/`);
        setClassDetail(classData[0]);
    }

    const getSlot = async () => {
        const slotData = await GetDataFromRoute(`slot${params.idSlot}/`);
        setSlotInfomation(slotData[0]);
    }

    const getStudent = async () => {
        const studentsData = await GetDataFromRoute(`studentsClass${params.idClass}/`);
        setStudents(studentsData);
    }

    return <Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList currnentKey={'activity'} />
        </Sider>
        <div className="attendent-information">
            <Card
                title="Class Information"
                className="class-container"
                bordered={false}
            >
                <p className="slot-name">Subject: {slotInfomation.subject}</p>
                <p className="slot-class">ClassId: {slotInfomation.class_id} </p>
                <p className="slot-date">Date: {slotInfomation.time_start} - {slotInfomation.time_end}</p>
            </Card>
            <Steps
                current={current}
                onChange={onChange}
                items={[
                    {
                        title: 'Step 1',
                        description,
                    },
                    {
                        title: 'Step 2',
                        description,
                    },
                    {
                        title: 'Step 3',
                        description,
                    },
                ]}
            />
        </div>
    </Layout>
}

export default Attendent