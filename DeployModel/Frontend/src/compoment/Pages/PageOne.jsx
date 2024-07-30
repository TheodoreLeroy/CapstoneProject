import React, { useState, useEffect } from "react";
import "./PageOne.css";

const PageOne = ({ students, onButtonClick }) => {
    const [numberAttendet, setNumberAttendet] = useState(3);
    const [totalStudent, setTotalStudent] = useState(0);
    const [linkImage, setLinkImage] = useState("../../../../DeployModel/Backend/");

    useEffect(() => {
        getTotalStudent();
    });

    const getTotalStudent = () =>{
        setTotalStudent(students.length);
        setNumberAttendet(students.length);
    }

    return (
        <main
            className="class-container"
        >
            <div style={{ width: "100%" }}>
                <h2>Class attendent</h2>
                <p>attendented: {numberAttendet}/{totalStudent}</p>
                <table className="table-container">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Id</th>
                            <th>Image</th>
                        </tr>
                    </thead>
                    <tbody>
                        {students?.map((student) =>(
                            <tr key={student.student_id}>
                                <td>{student.name}</td>
                                <td>{student.student_id}</td>                              
                                <td>{student.class_id}</td>
                                {/* <td><img src={linkImage.concat(student.StuImg.toString())} alt="Member 1" /></td> */}
                            </tr>
                        ))}                       
                    </tbody>
                </table>
            </div>
        </main>
    );
};

export default PageOne;
