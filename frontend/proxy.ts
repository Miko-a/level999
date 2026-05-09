import { NextRequest, NextResponse } from "next/server";

const ADMIN_SESSION_VALUE =
  process.env.ADMIN_SESSION_VALUE ?? "hsr-admin-session";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const isAdminLoginPage = pathname === "/admin/login";
  const session = request.cookies.get("admin_session")?.value;
  const isAuthenticated = session === ADMIN_SESSION_VALUE;

  if (pathname.startsWith("/admin") && !isAdminLoginPage && !isAuthenticated) {
    const loginUrl = request.nextUrl.clone();

    loginUrl.pathname = "/admin/login";
    loginUrl.searchParams.set("from", pathname);

    return NextResponse.redirect(loginUrl);
  }

  if (isAdminLoginPage && isAuthenticated) {
    const adminUrl = request.nextUrl.clone();

    adminUrl.pathname = "/admin";
    adminUrl.searchParams.delete("from");

    return NextResponse.redirect(adminUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*"],
};