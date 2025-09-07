import React,{useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
function NewProjectForm() {
    const [projectName,setProjectName]=useState('');
    const [projectDescription, setProjectDescription]=useState('');
    const [message, setMessage]=useState('');
    const [isError, setIsError]=useState(false);
    const navigate=useNavigate();
    const handleSubmit = async(e)=>{
        e.preventDefault();
        const token = localStorage.getItem('token');
        if(!token) {
            navigate('/login');
            return;
        }
        try {
            await axios.post(
                'https://heavily-blonde-coming-destroy.trycloudflare.com/api/projects',
                {
                    name:projectName,
                    description:projectDescription,
                },
                {
                    headers:{
                        'Authorization':`Bearer ${token}`
                    }
                }
            );
            setMessage('Project created successfully!');
            setIsError(false);
            setProjectName('');
            setProjectDescription('');
            setTimeout(()=> {
                navigate('/projects');
            }, 2000);

        } catch(error) {
            setMessage('Failed to create project. Please try again.');
            setIsError(true);
            console.error('Error creating project:', error.response ? error.response.data : error.message);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Create New Project</h2>
            {message&&<p className={isError ? "error-message" : "success-message"}>{message}</p>
            <label htmlFor="projectName">Project Name:</label>
            <input
                type="text"
                id="projectName"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                required
            />
            <label htmlFor="projectDescription">Description:</label>
            <textarea
                id="projectDescription"
                value={projectDescription}
                onChange={(e)=>setProjectDescription(e.target.value)}
                required
            ></textarea>
            <button type="submit">Create Project</button>
        </form>
    );
}
export default NewProjectForm;


