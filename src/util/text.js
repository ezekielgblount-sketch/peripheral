// Buyer-name handling. The name is entered on the menu, lives only in
// localStorage, and is never transmitted. These two helpers are the single
// source of truth for how it is cleaned and how it is shown on signage.

// Allowed: letters, space, hyphen, apostrophe. Trim, cap at 22. Deliberately
// gentle — a player who types a joke should get their joke on the sign.
export function sanitiseBuyer(raw) {
  return (raw || '')
    .replace(/[^A-Za-z \-']/g, '')
    .replace(/\s+/g, ' ')
    .slice(0, 22)
    .replace(/^\s+/, '');
}

// What actually gets painted: uppercased, with a deliberate fallback.
export function buyerDisplay(raw) {
  const s = sanitiseBuyer(raw).trim();
  return (s || 'NEW OWNER').toUpperCase();
}
