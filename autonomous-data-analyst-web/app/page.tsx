import { Sidebar, MobileBar } from "@/components/sidebar";
import { Workspace } from "@/components/workspace";

export default function Page() {
  return (
    <div className="min-h-dvh lg:grid lg:grid-cols-[248px_minmax(0,1fr)]">
      <Sidebar />
      <MobileBar />
      <main className="min-w-0">
        <Workspace />
      </main>
    </div>
  );
}
