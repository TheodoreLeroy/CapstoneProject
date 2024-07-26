import React, {useState} from "react";
import "./PageOne.css";

const PageOne = ({ onButtonClick }) => {
    const [numberAttendet, setNumberAttendet] = useState(3);
    const [totalStudent, setTotalStudent] = useState(3);

    return (
        <main
            className="class-container"
        >
            <div style={{width: "100%"}}>
                <h2>Class attendent</h2>
                <p>attendented: {numberAttendet}/{totalStudent}</p>
                <table className="table-container">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Id</th>
                            <th>Image</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>                          
                            <td>Vũ</td>
                            <td>HE161744</td>
                            <td><img src="path/to/image1.jpg" alt="Member 1" /></td>
                        </tr>
                        <tr>
                            <td>Lương</td>
                            <td>HE163772</td>
                            <td><img src="path/to/image2.jpg" alt="Member 2"/></td>                           
                        </tr>
                        <tr>
                            <td>Nguyễn</td>
                            <td>HE163853</td>
                            <td><img src="path/to/image3.jpg" alt="Member 3"/></td>                           
                        </tr>
                    </tbody>
                </table>
            </div>
        </main>
    );
};

export default PageOne;
