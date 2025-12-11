import axios from "axios"

const service = axios.create({
    baseURL: 'http://127.0.0.1:8000/', // 这里改为 baseURL
    timeout: 40000,
})

export default service