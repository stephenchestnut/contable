
package contable

import breeze.linalg._

class Margins(val row_sums: Seq[Int], val col_sums: Seq[Int]) {

  val r = new DenseVector(row_sums.toArray)
  val c = new DenseVector(col_sums.toArray)
  val m = r.length
  val n = c.length

  def isFeasible = true

  def check(X: DenseMatrix[Int]) = 
    ((X.rows == m) && (X.cols == n)
     && (sum(X,Axis._0) == r.toDenseMatrix)
     && (sum(X,Axis._1) == c))
}
