import { NavLink } from "react-router";

export default function NavButton({ to, icon: Icon }: { to: string; icon: React.ElementType }) {
  console.log(Icon);
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `rounded-lg p-2 ${
          isActive
            ? "bg-neutral-50 dark:bg-neutral-700"
            : "text-slate-600 hover:bg-slate-200 hover:text-slate-900"
        }`
      }
    >
      <Icon className="h-full w-full" />
    </NavLink>
  );
}
