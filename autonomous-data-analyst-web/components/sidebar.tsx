import { ApiStatus } from "./api-status";

const WORKSPACE = ["Analysis", "Datasets", "Sessions", "Reports"] as const;
const SYSTEM = ["Trace", "Evaluation"] as const;

function NavGroup({ label, items, active }: { label: string; items: readonly string[]; active?: string }) {
  return (
    <div>
      <p className="mono-label !text-white/40">{label}</p>
      <ul className="mt-3 space-y-px">
        {items.map((item) =>
          item === active ? (
            <li key={item}>
              <span
                aria-current="page"
                className="block border-l border-white py-1.5 pl-3 text-[15px] font-medium text-white"
              >
                {item}
              </span>
            </li>
          ) : (
            <li key={item}>
              {/* Only Analysis exists in this build; the rest are not wired to routes. */}
              <span
                aria-disabled="true"
                title="Not available yet"
                className="block cursor-default border-l border-transparent py-1.5 pl-3 text-[15px] text-white/35"
              >
                {item}
              </span>
            </li>
          ),
        )}
      </ul>
    </div>
  );
}

export function Sidebar() {
  return (
    <aside className="sticky top-0 hidden h-dvh flex-col justify-between bg-ink px-7 py-8 text-white lg:flex">
      <div className="space-y-12">
        <div>
          <p className="text-[28px] font-semibold leading-none tracking-[0.04em]">NOHA</p>
          <p className="mono-label mt-3 !text-white/50">Autonomous Data Analyst</p>
        </div>
        <nav aria-label="Primary" className="space-y-9">
          <NavGroup label="Workspace" items={WORKSPACE} active="Analysis" />
          <NavGroup label="System" items={SYSTEM} />
        </nav>
      </div>
      <ApiStatus />
    </aside>
  );
}

export function MobileBar() {
  return (
    <header className="flex items-center justify-between bg-ink px-5 py-4 text-white lg:hidden">
      <p className="text-lg font-semibold tracking-[0.04em]">NOHA</p>
      <ApiStatus />
    </header>
  );
}
