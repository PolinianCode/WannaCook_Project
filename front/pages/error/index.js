import Header from "../../components/Header/HeaderComponent"
import Container from "../../components/Basic/ContainerComponent"
import NotFound from "../../components/Basic/404"
import { useRouter } from "next/router";

export default function Error() { 

    const router = useRouter();

    const { code, message } = router.query;

    return (
        <div>
            <Header />
            <Container>
                <NotFound headingTitle={`Error ${code}`} pageText={message}/>
            </Container>
        </div>
    )
}