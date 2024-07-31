import FormSlot from "../compoment/FormSlot"
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import GetDataFromRoute from "../compoment/GetDataFromBackend";

import { useNavigate, useParams } from "react-router-dom";
import { Layout } from "antd";
const { Sider } = Layout
import { useEffect, useState } from "react";


import "../styles/Class.css";
import "../styles/Sidebar.css";


function NewSlot() {
    const { idClass } = useParams();
    const [slots, setSlots] = useState([]);
    const [classDetail, setClassDetail] = useState({});

    const navigate = useNavigate()

    useEffect(() => {
        getSlot();
        getClass();
    }, [])

    const getSlot = async () => {
        const slotData = await GetDataFromRoute(`class${idClass}/slot/`)
        setSlots(slotData)
    }
    const getClass = async () => {
        const classData = await GetDataFromRoute(`class${idClass}/`)
        setClassDetail(classData[0])
    }

    const handlerClick =(idSlot) =>{
        navigate(`/class/${idClass}/slot/${idSlot}`)
    }

    return (<Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList currnentKey={'create_class'} />
        </Sider>
        <div className="class-information">
            <div className="class-container">
                <h2>Class Information</h2>
                <p className="class-number">Class name: {classDetail.class_name}</p>
                <p className="class's-slot">Semester: {classDetail.semester}</p>
            </div>
            <div className="slots-class-container">
                <div className="slot-container">
                    <h2 className="class's-slot">Slots: </h2>
                    <div className="all-slots">
                        {slots.map((slot) => (
                            <div key={slot.id} id="one-slot-container" onClick={() => handlerClick(slot.id)}>
                                <p className="class-number">subject: {slot.subject}</p>
                                <p className="class-semester">Time: {slot.time_start} - {slot.time_end}</p>
                            </div>
                        ))}
                    </div>
                </div>
                <FormSlot route={`class${idClass}/createSlot`}></FormSlot >
            </div>
        </div>
    </Layout>
    )
}

export default NewSlot