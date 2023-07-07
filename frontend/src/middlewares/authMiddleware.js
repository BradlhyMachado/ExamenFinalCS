export function authProfesores(to, from, next) {
    const token = localStorage.getItem('token');
    const nombreGrupo = localStorage.getItem('nombre_grupo');

    if (token && nombreGrupo === 'Profesores') {
      next();
    } else {
      next('/login'); // Change '/login' to the path of the login page
    }
}

export function authEstudiantes(to, from, next) {
    const token = localStorage.getItem('token');
    const nombreGrupo = localStorage.getItem('nombre_grupo');
      
    console.log('Middleware');
  
    if (token && nombreGrupo === 'Estudiantes') {
      next();
    } else {
      next('/login'); // Change '/login' to the path of the login page
    }
}

export function authAdmin(to, from, next) {
  const token = localStorage.getItem('token');
  const nombreGrupo = localStorage.getItem('nombre_grupo');
    
  console.log('Middleware');

  if (token && nombreGrupo === 'Administrador') {
    next();
  } else {
    next('/login'); // Change '/login' to the path of the login page
  }
}