
package contable

import breeze.linalg._
import breeze.numerics._

class Margins(row_sums: Vector[Int], col_sums: Vector[Int]) {

  val r = row_sums.toDenseVector
  val c = col_sums.toDenseVector
  val m = r.length
  val n = c.length

  def isFeasible = ( (m>0) && (n>0) && (sum(r) == sum(c)) && all(r :>= 0) && all(c :>= 0) )

  def check(X: DenseMatrix[Int]) = 
    ((X.rows == m) && (X.cols == n)
     && (sum(X,Axis._0) == r.toDenseMatrix)
     && (sum(X,Axis._1) == c))
}

class MarginsWithCellBounds(row_sums: DenseVector[Int], 
                            col_sums: DenseVector[Int],
                            bounds: Matrix[Int]) extends Margins(row_sums,col_sums) {
  val B = bounds.toDenseMatrix

  override def isFeasible: Boolean = super.isFeasible //check the flow problem instead

  override def check(X: DenseMatrix[Int]) = (super.check(X) && all(X :<= B))

}
