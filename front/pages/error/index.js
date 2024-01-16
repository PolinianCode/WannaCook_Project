import NotFound from "../../components/Basic/404"
import { useRouter } from "next/router";
import Layout from "../../components/layout";
import Head from 'next/head';

export default function Error() { 

    const router = useRouter();

    const { code, message } = router.query;

    return (
        <Layout>
            <Head>
                <title>Error {code}</title>
            </Head>
            <NotFound headingTitle={`Error ${code}`} pageText={message}/>
        </Layout>
    )
}