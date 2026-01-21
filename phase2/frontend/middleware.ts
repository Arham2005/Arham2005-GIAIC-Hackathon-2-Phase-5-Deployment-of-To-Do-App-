import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect routes
export function middleware(request: NextRequest) {
  // Only handle specific redirects, don't check authentication for protected routes
  // Authentication will be handled client-side

  // If user is authenticated (has token) and trying to access login/signup, redirect to dashboard
  let token = request.cookies.get('auth_token')?.value;
  if (!token) {
    // Check if token is passed in the Authorization header
    const authHeader = request.headers.get('authorization');
    if (authHeader && authHeader.startsWith('Bearer ')) {
      token = authHeader.substring(7, authHeader.length);
    }
  }

  const isLoginPage = request.nextUrl.pathname === '/login' || request.nextUrl.pathname === '/signup';
  if (token && isLoginPage) {
    console.log(`Middleware: Authenticated user trying to access login, redirecting to dashboard`);
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Allow all other requests to proceed - let client-side handle authentication
  return NextResponse.next();
}

// Apply middleware to all routes except static assets and API routes
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - tasks (API routes)
     * - auth (API routes)
     */
    {
      source: '/((?!api|auth|tasks|_next/static|_next/image|favicon.ico).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },
  ],
};