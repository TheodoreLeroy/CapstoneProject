import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import GetDataFromRoute from "../compoment/GetDataFromBackend";
import api from "../api";
import LoadingIndicator from "../compoment/LoadingIndicator";

import { useNavigate, useParams } from "react-router-dom";
import { notification, TimePicker, Layout } from "antd";
const { Sider } = Layout
import { useEffect, useState } from "react";
import { CSSTransition } from 'react-transition-group';
import dayjs from 'dayjs';


import "../styles/Class.css";
import "../styles/Sidebar.css";
import "../styles/FormSlot.css";


function NewSlot() {
    const { idClass } = useParams();
    const [slots, setSlots] = useState([]);
    const [classDetail, setClassDetail] = useState({});
    const [students, setStudents] = useState([]);

    const [class_id, setClassId] = useState(idClass);
    const [subject, setSubject] = useState("");
    const [time_start, setTimeStart] = useState("");
    const [time_end, setTimeEnd] = useState(null);
    const [loading, setLoading] = useState(false);

    const [name, setNewStudent] = useState("");

    const [inProp, setInProp] = useState(false);

    const message = "Create new slot";

    const navigate = useNavigate()

    useEffect(() => {
        getSlot();
        getClass();
        getStudent();

    }, [])

    const getSlot = async () => {
        const slotData = await GetDataFromRoute(`class${idClass}/slot/`)
        setSlots(slotData)
    }
    const getClass = async () => {
        const classData = await GetDataFromRoute(`class${idClass}/`)
        setClassDetail(classData[0])
    }
    const getStudent = async () => {
        const studentsData = await GetDataFromRoute(`studentsClass${idClass}/`)
        setStudents(studentsData)
    }
    const handlerClick = (idSlot) => {
        navigate(`/class/${idClass}/slot/${idSlot}`)
    }

    const handleSubmitSlot = async (e) => {
        setLoading(true);
        e.preventDefault();
        try {
            const res = await api.post(`class${idClass}/createSlot`, { class_id, subject, time_start, time_end });
            if (res.status === 201) {
                notification.success({
                    message: 'Success',
                    description: `Slot created successfully!
                            Please refrest to see it in class`,
                    placement: 'topRight',
                    duration: 3,
                });

                setInProp(true);
                getSlot();
            }
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false);
            setInProp(false);
        }
    };

    const handleSubmitStudent = async (e) => {
        setLoading(true);
        e.preventDefault();
        const email = name.concat('', (students.length + 1)).concat('', "@gmail.com")
        const password = "123456"
        try {
            const res = await api.post(`studentsClass${idClass}/`, { name, email, password, class_id });
            if (res.status === 201) {
                notification.success({
                    message: 'Success',
                    description: `Slot created successfully!
                            Please refrest to see it in class`,
                    placement: 'topRight',
                    duration: 3,
                });
                getStudent();
            }
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false);
            setInProp(false);
        }
    };

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
                <p className="class's-slot">Total student: {students.length}</p>
            </div>
            <div className="slots-class-container">
                <div className="slot-container">
                    <h2 className="class's-slot">Slots: </h2>
                    <div className="all-slots">

                        {slots.map((slot) => (
                            <CSSTransition in={inProp} timeout={1000} classNames="fade" key={slot.id}>
                                <div  id="one-slot-container" onClick={() => handlerClick(slot.id)}>
                                    <p className="class-number">subject: {slot.subject}</p>
                                    <p className="class-semester">Time: {slot.time_start} - {slot.time_end}</p>
                                </div>
                            </CSSTransition>
                        ))}
                    </div>
                </div>
                <div>
                    <form onSubmit={handleSubmitSlot} className="form-container">
                        <h1>{message}</h1>
                        <input
                            className="form-input"
                            type="text"
                            value={subject}
                            onChange={(e) => setSubject(e.target.value)}
                            placeholder="Subject"
                        />
                        <TimePicker.RangePicker
                            className="timePicker"
                            format="HH:mm"
                            onChange={(e) => {
                                setTimeStart(e[0].format('HH:mm:ss'));
                                setTimeEnd(e[1].format('HH:mm:ss'));
                            }}
                            defaultValue={[
                                dayjs('00:00', 'HH:mm'),
                                dayjs('00:00', 'HH:mm'),
                            ]}
                        />
                        {loading && <LoadingIndicator />}
                        <button className="form-button" type="submit">
                            {message}
                        </button>
                    </form>
                    <form onSubmit={handleSubmitStudent} className="form-container">
                        <h1>Add new student</h1>
                        <input
                            className="form-input"
                            type="text"
                            value={name}
                            onChange={(e) => setNewStudent(e.target.value)}
                            placeholder="Subject"
                        />
                        {loading && <LoadingIndicator />}
                        <button className="form-button" type="submit">
                            Add new student
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </Layout>
    )
}

export default NewSlot