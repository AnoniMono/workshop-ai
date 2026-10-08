export interface StatSide {
  /** numero grande, es. "100.000 miliardi" */
  value: string;
  /** spiegazione breve sotto il numero */
  caption: string;
}

export interface StatCompareProps {
  /** argomento, es. "Connessioni" */
  topic: string;
  brain: StatSide;
  machine: StatSide;
  /** frase finale: chi vince e di quanto */
  takeaway: string;
}

/** Confronto cervello contro macchina: due numeri grandi (rosa = cervello, ciano = macchina) e una conclusione. */
export function StatCompare({ topic, brain, machine, takeaway }: StatCompareProps) {
  return (
    <div className="ws-stat">
      <p className="ws-stat__topic">{topic}</p>
      <p className="ws-stat__row is-brain"><b>{brain.value}</b><span>{brain.caption}</span></p>
      <p className="ws-stat__row is-machine"><b>{machine.value}</b><span>{machine.caption}</span></p>
      <p className="ws-stat__take">{takeaway}</p>
    </div>
  );
}
