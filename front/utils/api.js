export default function JSONtoURL(json, url_path) {
    const url = `http://localhost:8000/api/${url_path}`
    const data = encodeURIComponent(JSON.stringify(json));
    return `${url}?data=${data}`;
}