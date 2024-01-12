import NotFound from "../../components/Basic/404"
import { useRouter } from "next/router";
import Layout from "../../components/layout";

export default function Error() { 

    const router = useRouter();

    const { code, message } = router.query;

    return (
        <Layout>
            <NotFound headingTitle={`Error ${code}`} pageText={message}/>
        </Layout>
    )
}