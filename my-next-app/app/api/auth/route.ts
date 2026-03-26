import { NextRequest, NextResponse } from 'next/server'

const USERNAME = 'msutanto'
const PASSWORD = 'password$01'

export async function POST(req: NextRequest) {
  const { username, password } = await req.json()

  if (username === USERNAME && password === PASSWORD) {
    const res = NextResponse.json({ ok: true })
    res.cookies.set('auth', 'authenticated', {
      httpOnly: true,
      sameSite: 'lax',
      path: '/',
    })
    return res
  }

  return NextResponse.json({ ok: false, error: 'Invalid credentials' }, { status: 401 })
}

export async function DELETE() {
  const res = NextResponse.json({ ok: true })
  res.cookies.delete('auth')
  return res
}
