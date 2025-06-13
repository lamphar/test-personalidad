
export function analyse(test, pct){
  const blocks = {
    'Estoicismo': [
      {max:40, title:'Bajo autocontrol', text:'Puedes beneficiarte de practicar técnicas de respiración y journaling.', color:'#EF4444'},
      {max:70, title:'Equilibrio', text:'Buen progreso. Mantén tu rutina de reflexión diaria.', color:'#F59E0B'},
      {max:101, title:'Alto dominio', text:'Excelente autocontrol y aceptación.', color:'#10B981'}
    ],
    'Autoestima': [
      {max:40,title:'Autoestima baja', text:'Trabaja afirmaciones positivas y terapia cognitiva.', color:'#EF4444'},
      {max:70,title:'Autoestima media', text:'Sigue reforzando tus logros y gratitud diaria.', color:'#F59E0B'},
      {max:101,title:'Autoestima alta', text:'Tu autoconfianza es sólida. Continúa potenciando tus talentos.', color:'#10B981'}
    ],
    'Resiliencia': [
      {max:40,title:'Resiliencia baja', text:'Aprende técnicas de afrontamiento y apoyo social.', color:'#EF4444'},
      {max:70,title:'Resiliencia media', text:'Buen punto de partida. Consolidar redes de apoyo te ayudará.', color:'#F59E0B'},
      {max:101,title:'Resiliencia alta', text:'Tienes gran capacidad para superar adversidades.', color:'#10B981'}
    ]
  };
  const row = blocks[test].find(b=>pct<=b.max);
  return row;
}
