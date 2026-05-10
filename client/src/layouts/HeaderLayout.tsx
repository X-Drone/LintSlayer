import { Outlet } from "react-router"
import Header from "../components/Header";
import AnimatedBackground from "../components/AnimatedBackground";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export default function HeaderLayout()
{
    return(
        <QueryClientProvider client={queryClient}>
            <div className="relative min-h-screen max-w-full flex flex-col">
                <AnimatedBackground />
                <Header/>
                <main className="relative flex-1">
                    <Outlet/>
                </main>
            </div>
        </QueryClientProvider>
    );
}
