
package contable

import breeze.linalg._

class Margins(row_sums: Seq[Int], col_sums: Seq[Int]) {

  val r = new DenseVector(row_sums.toArray)
  val c = new DenseVector(col_sums.toArray)
  val m = r.length
  val n = c.length

  def isFeasible = ( (m>0) && (n>0) && (sum(r) == sum(c)) && all(r :>= 0) && all(c :>= 0) )

  def check(X: DenseMatrix[Int]) = 
    ((X.rows == m) && (X.cols == n)
     && (sum(X,Axis._0) == r.toDenseMatrix)
     && (sum(X,Axis._1) == c))
}

class MarginsWithCellBounds(row_sums: Seq[Int], 
                            col_sums: Seq[Int],
                            cell_bounds: Matrix[Int]) extends Margins(row_sums,col_sums) {

  val B = cell_bounds.toDenseMatrix

  override def isFeasible = super.isFeasible //check the flow problem instead

  override def check(X: DenseMatrix[Int]) = (super.isFeasible && all(X :<= B))

}
