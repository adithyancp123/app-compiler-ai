type NavItem = {
  id: string;
  label: string;
  icon: string;
};

type SidebarNavProps = {
  items: NavItem[];
  activeId: string;
  onChange: (id: string) => void;
};

export default function SidebarNav({ items, activeId, onChange }: SidebarNavProps) {
  return (
    <aside className="rounded-2xl border border-slate-200 bg-white/70 p-2 shadow-sm backdrop-blur">
      <p className="px-3 py-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Workspace</p>
      <div className="space-y-1">
        {items.map((item) => {
          const active = item.id === activeId;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => onChange(item.id)}
              className={[
                "group flex w-full items-center gap-2 rounded-xl px-3 py-2 text-left text-sm transition",
                active
                  ? "relative bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-sm"
                  : "text-slate-700 hover:bg-slate-100",
              ].join(" ")}
            >
              {active ? <span className="absolute left-1.5 h-5 w-1 rounded-full bg-white/80" /> : null}
              <span className={active ? "text-white" : "text-slate-500 group-hover:text-slate-700"}>{item.icon}</span>
              <span className="text-[13px] font-semibold">{item.label}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
}

