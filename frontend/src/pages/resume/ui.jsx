export const initials = (name) =>
  (name || '?').split(' ').filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join('');

export function Ring({ value, label, suffix = '', small, light }) {
  return (
    <div className={`rs-ring${small ? ' rs-ring-sm' : ''}${light ? ' rs-ring-light' : ''}`} style={{ '--p': value }}>
      <div className="rs-ring-bar" />
      <div className="rs-ring-in">
        <b>{value}{suffix}</b>
        {label && <small>{label}</small>}
      </div>
    </div>
  );
}

export function Head({ icon, title, extra }) {
  return (
    <div className="rs-card-head">
      <div className="rs-ico">{icon}</div>
      <h3>{title}</h3>
      {extra && <span className="rs-count">{extra}</span>}
    </div>
  );
}