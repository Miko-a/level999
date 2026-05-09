import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import AdminClient from "./AdminClient";

const ADMIN_SESSION_VALUE =
  process.env.ADMIN_SESSION_VALUE ?? "hsr-admin-session";

export default async function AdminPage() {
  const cookieStore = await cookies();
  const session = cookieStore.get("admin_session")?.value;

  if (session !== ADMIN_SESSION_VALUE) {
    redirect("/admin/login?from=/admin");
  }

  return <AdminClient />;
}